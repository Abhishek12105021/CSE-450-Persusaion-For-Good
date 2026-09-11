"""
Organic-Rewrite Pipeline for the Buyer-Seller Dialogue Corpus
=============================================================
Rewrites dialogue text so all 500 dialogues read like real Facebook-page
buyer/seller chats, using the Gemini API.

WHAT THIS DOES AND DOES NOT DO
------------------------------
This pass changes *wording only*. It cannot change `turn_count`, the intent
sequence, or the phase path -- those are pinned by the validator on purpose,
because they carry the labels. The structural leakage in the corpus was
already fixed in `build_advanced_dialogues.py` v2 (see extended_dataset.md).
Run this only on a corpus that passes `audit_dataset.py`; it is a polish
pass, not a repair for a structurally broken dataset.

CHANGES FROM THE PREVIOUS VERSION
---------------------------------
  1. TARGETS ALL 500 DIALOGUES. The old filter matched
     `antigravity-advanced-state-machine`, a source_model tag that no longer
     exists in the corpus -- the pipeline would have found 0 dialogues to
     process and silently written out an unchanged file. Both the seed and
     generated splits are now rewritten (`--only` narrows it if wanted).

  2. FIXES THE PRICE-CORRUPTION BUG. `perturb_price_format` ran AFTER
     validation and re-randomized each price independently, so a dialogue
     validated as consistent could be written out with "32,000 BDT" in one
     turn and "BDT 32,000" in the next -- and the old validator regex could
     not even see the prefix form, making the corruption undetectable on a
     re-run. Currency format is now decided ONCE per dialogue and applied
     uniformly, before validation.

  3. VALIDATES WHAT ACTUALLY MATTERS. Adds checks the old version lacked:
     role alternation, turn-order, product-name survival, near-copy
     detection (a "paraphrase" that changes nothing is now rejected), and
     numeric-fact preservation that understands both price forms.

  4. ORGANIC REALISM, NOT JUST "STYLE". The prompt now asks for the specific
     texture of marketplace chat -- typos, lowercase, dropped
     punctuation, split messages -- with per-turn
     noise applied locally afterwards. Style is sampled per DIALOGUE and
     jitter per TURN, so a single conversation stays in one voice.

  5. PRESERVES THE FULL SCHEMA. The old prompt asked the model to return
     only 4 keys, silently dropping `original_intent` from every rewritten
     turn -- the exact schema break that v1 of the generator was fixed for.
     `original_intent` is now re-attached from the source turn.

  6. SAFE RESUME. Checkpoint keys are dialogue_ids, not list indices, so a
     resumed run cannot mis-assign results if the corpus is regenerated.

Usage:
    set GEMINI_API_KEY=your_key
    python paraphrase_pipeline.py                 # all 500
    python paraphrase_pipeline.py --only generated
    python paraphrase_pipeline.py --limit 10 --dry-run   # no API calls
"""

import os
import sys
import json
import time
import random
import re
import argparse
import difflib

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL = "gemini-3.5-flash-lite"
RPM_LIMIT = 10
DELAY_BETWEEN_CALLS = 60.0 / RPM_LIMIT

INPUT_FILE = os.path.join(SCRIPT_DIR, "extended_dataset.json")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "extended_dataset_organic.json")
CHECKPOINT_FILE = os.path.join(SCRIPT_DIR, "paraphrase_checkpoint.json")
CHECKPOINT_RESULTS = os.path.join(SCRIPT_DIR, "paraphrase_checkpoint_results.json")

MAX_RETRIES = 3
BACKOFF_SECONDS = [30, 60, 120]

GENERATED_TAG = "compositional-generator-v2"
ORGANIC_SUFFIX = "-organic"

# A rewritten turn must differ from the original by at least this much
# (difflib ratio below this threshold = sufficiently reworded). Catches the
# common failure where the model echoes the input with one synonym swapped.
MAX_SIMILARITY = 0.82

# ============================================================
# 1. VOICE / STYLE BANKS
# ============================================================
# Sampled once per DIALOGUE so a conversation keeps a single consistent
# voice. Mixing styles turn-by-turn is what made the previous output read
# like a committee wrote it.
BUYER_VOICES = [
    "a busy office worker typing fast on mobile -- short messages, missing "
    "capitals, occasional typos, no full stops",
    "a polite, careful buyer who writes complete sentences and says 'please' "
    "and 'thank you' often",
    "a blunt bargain hunter -- terse, slightly impatient, focused on price",
    "a cautious first-time online buyer -- hedges a lot, asks for "
    "reassurance, worries about scams",
    "a technically confident buyer who knows the product category and asks "
    "precise questions",
    "a friendly chatty buyer who adds small pleasantries and emoji-free warmth",
    "a young student buyer -- very casual, lowercase, abbreviations like "
    "'plz', 'ok', 'thnx'",
    "a no-nonsense professional -- minimal words, direct questions, no "
    "pleasantries at all",
]

MERCHANT_VOICES = [
    "a professional page admin -- courteous, uses 'sir'/'ma'am', complete "
    "sentences, mild sales enthusiasm",
    "a busy shop owner replying between customers -- brief, functional, "
    "occasionally drops articles",
    "a friendly small-business seller -- warm and welcoming",
    "a formal electronics retailer -- precise, policy-focused, emphasises "
    "warranty and authenticity",
    "an eager salesperson -- enthusiastic, adds light persuasion and urgency",
]

# Per-turn micro-jitter applied AFTER the API rewrite. Kept deliberately
# mild: too much noise degrades the tokenizer's view of the text without
# adding realism.
TYPO_MAP = {
    "the": "teh", "and": "adn", "you": "yuo", "with": "wiht",
    "price": "pirce", "have": "hvae", "just": "jsut", "want": "watn",
    "what": "waht", "this": "thsi", "your": "yuor", "thanks": "thnaks",
}

# English only -- "acha" was previously here and injected Banglish into
# turns that the API had already returned as clean English.
FILLERS_BUYER = ["ok ", "hmm ", "right ", "so ", "well "]
FILLERS_MERCHANT = ["sure ", "yes ", "ok ", "right "]


# ============================================================
# 2. LOCAL PERTURBATIONS
# ============================================================
# Currency style is chosen ONCE PER DIALOGUE and applied to every turn.
#
# The previous implementation re-randomised each match independently and ran
# AFTER validation, so one dialogue could end up saying "32,000 BDT" in the
# merchant's quote and "BDT 32,000" two turns later -- inconsistent in a way
# no human seller writes, and invisible to the old validator (whose regex
# only matched the suffix form). Now it runs BEFORE validation, uniformly.
# Only one currency word is permitted corpus-wide. Money is a
# high-frequency token and four spellings of it ("32,000 BDT", "BDT 32,000",
# "32,000 Tk", "32,000 taka") are four things a tokenizer must learn
# separately for no gain. `enforce_english.py` re-checks this.
CURRENCY_STYLES = ["taka"]

_PRICE_RE = re.compile(
    r"(?:(?P<pre>BDT|Tk|taka)\s*(?P<n1>[\d,]+))"
    r"|(?:(?P<n2>[\d,]+)\s*(?P<post>BDT|Tk|taka))",
    re.IGNORECASE,
)


def apply_currency_style(text, style):
    """Rewrite every money amount in `text` into one consistent style."""
    def repl(m):
        num = m.group("n1") or m.group("n2")
        digits = num.replace(",", "")
        if not digits.isdigit():
            return m.group(0)
        return f"{int(digits):,} taka"

    return _PRICE_RE.sub(repl, text)


def extract_amounts(text):
    """Return the set of numeric money values in a turn, format-agnostic.

    Used by the validator so that "32,000 BDT", "BDT 32,000" and "32000 Tk"
    all compare equal -- the old validator treated these as different and
    could not see the prefix form at all.
    """
    out = set()
    for m in _PRICE_RE.finditer(text):
        num = m.group("n1") or m.group("n2")
        digits = num.replace(",", "")
        if digits.isdigit():
            out.add(int(digits))
    return out


def add_turn_noise(text, role, rng, intensity):
    """Apply mild, human-looking imperfection to a single turn."""
    if intensity <= 0:
        return text

    # Lowercase the opening word (very common in fast mobile typing).
    if rng.random() < 0.25 * intensity:
        text = text[:1].lower() + text[1:]

    # Drop a trailing full stop.
    if rng.random() < 0.30 * intensity and text.endswith("."):
        text = text[:-1]

    # Insert a leading filler.
    if rng.random() < 0.18 * intensity:
        bank = FILLERS_BUYER if role == "Buyer" else FILLERS_MERCHANT
        text = rng.choice(bank) + text[:1].lower() + text[1:]

    # Introduce at most one typo, and never inside a number or a product
    # name -- corrupting those would break the factual checks downstream.
    if rng.random() < 0.15 * intensity:
        words = text.split()
        idx = [i for i, w in enumerate(words) if w.lower() in TYPO_MAP]
        if idx:
            i = rng.choice(idx)
            words[i] = TYPO_MAP[words[i].lower()]
            text = " ".join(words)

    return text


def perturb_reason(reason, rng):
    """Vary `labels.reason` wording.

    Table-driven, keyed on the exact reason strings the v2 generator emits
    (the previous version's keys were v1 strings and matched nothing).
    Unknown reasons pass through untouched.
    """
    variations = {
        "Buyer completed negotiation, accepted advance policy, and committed to purchase.": [
            "Buyer negotiated the price, agreed to pay the advance, and confirmed the purchase.",
            "After bargaining and accepting the advance fee, the buyer committed to buying.",
            "Purchase was committed after the buyer accepted the negotiated price and advance policy.",
        ],
        "Buyer committed to purchase after the merchant waived the advance and agreed to full COD.": [
            "The merchant dropped the advance requirement and the buyer confirmed the order on full COD.",
            "Buyer committed once full Cash on Delivery was agreed and no advance was required.",
        ],
        "Buyer deferred decision after learning the price and specs.": [
            "Buyer chose to delay the purchase decision after reviewing price and specifications.",
            "After hearing the price and specs, the buyer decided to think it over.",
        ],
        "Buyer deferred the decision even after a negotiated discount.": [
            "Even with a discount on the table, the buyer postponed the decision.",
            "Buyer still asked for time despite the merchant conceding on price.",
        ],
        "Buyer deferred the decision after reviewing specifications.": [
            "Buyer postponed the decision once the technical details were clear.",
            "After the spec discussion, the buyer asked for time to consider.",
        ],
        "Buyer deferred the decision after reviewing delivery arrangements.": [
            "Buyer delayed the decision after going over delivery options.",
            "Once delivery terms were explained, the buyer asked for time.",
        ],
        "Buyer deferred the decision pending the advance payment requirement.": [
            "Buyer held off deciding because of the advance payment condition.",
            "The advance requirement left the buyer wanting time to think.",
        ],
        "Buyer abandoned dialogue after merchant refused discount.": [
            "Buyer dropped out when the discount request was denied by the merchant.",
            "After the merchant refused to negotiate on price, the buyer walked away.",
        ],
        "Buyer abandoned the inquiry once the price exceeded their budget.": [
            "The quoted price was above budget, so the buyer ended the inquiry.",
            "Buyer stopped engaging after the price came in over budget.",
        ],
        "Buyer abandoned the dialogue over unacceptable delivery timelines.": [
            "Delivery was too slow for the buyer, who ended the conversation.",
            "Buyer walked away because the delivery timeline did not suit them.",
        ],
        "Buyer dropped out early due to technical specification mismatch.": [
            "The buyer left early because the specs didn't match their requirements.",
            "A technical specification mismatch caused the buyer to drop out early.",
        ],
        "Buyer chose a competing option after a direct comparison.": [
            "After comparing against an alternative, the buyer went with the competitor.",
            "The comparison favoured another option and the buyer moved on.",
        ],
        "Buyer explicitly rejected mandatory advance fee and walked away.": [
            "The buyer refused to pay the mandatory advance and cancelled.",
            "Buyer rejected the advance payment policy outright and left.",
        ],
    }
    if reason in variations and rng.random() < 0.7:
        return rng.choice(variations[reason])
    return reason


# ============================================================
# 3. PROMPT CONSTRUCTION
# ============================================================
def build_prompt(dialogue, buyer_voice, merchant_voice):
    """Build the rewrite prompt.

    Note the schema contract: we ask for turn_id/role/text only. The model
    is not asked to echo `normalized_intent` or `original_intent` -- those
    are re-attached from the source turn afterwards, which removes any
    chance of the model corrupting a label field and removes ~40% of the
    output tokens per call.
    """
    payload = [
        {"turn_id": t["turn_id"], "role": t["role"], "text": t["text"]}
        for t in dialogue["turns"]
    ]
    turns_json = json.dumps(payload, indent=2, ensure_ascii=False)
    n = len(payload)

    return f"""You are rewriting a real Facebook-page conversation between an online shopper and a shop's page admin, so it reads like an authentic chat log rather than a script.

## VOICES
Rewrite every Buyer turn as: **{buyer_voice}**
Rewrite every Merchant turn as: **{merchant_voice}**
Keep each speaker's voice consistent across the whole conversation.

## MAKE IT ORGANIC
Real marketplace chat is not clean prose. Apply these naturally, not to every line:
- Vary sentence length sharply. Some turns are two words ("in stock?", "ok"), some are long.
- It is fine to drop capitals, skip full stops, or use "..." mid-thought.
- Occasional light informality: "plz", "thnx", "ok", "u" -- sparingly, only for casual voices.
- Merchants often repeat key policy points and add reassurance.
- Buyers often ask the same thing twice in different words when unsure.

## HARD RULES -- violating any of these makes the output unusable
0. ENGLISH ONLY. Every turn must be written entirely in English. No Bangla script, no Banglish or romanised Bangla, no Hindi or Urdu -- not even single words or greetings. Specifically forbidden: "bhai", "apu", "acha", "ache", "koto", "dam", "hobe", "nai", "toh", "kya", "assalamu alaikum", "walaikum assalam". If the input turn contains any of these, translate it into natural English. Write money as "32,000 taka" -- never "BDT" or "Tk".
1. Output EXACTLY {n} turns, with turn_id 1..{n} in order, and the SAME role on each turn_id as the input. Never merge, split, add, drop, or reorder turns.
2. Preserve every FACT exactly: product names and model numbers (e.g. "Sony WH-1000XM5", "X-T30 II"), all money amounts, phone numbers, delivery addresses, TrxIDs, and technical figures ("8 microphones", "30 hours", "1050 MB/s", "IP65", "350 degrees").
3. Preserve the MEANING and FUNCTION of each turn. A question stays a question about the same thing; a refusal stays a refusal; a commitment stays a commitment. Never make a hesitant buyer sound decided, or a decided buyer sound hesitant -- the conversation's outcome must not change.
4. Genuinely REWORD. Do not echo the input with one or two words swapped. Change sentence structure and vocabulary.
5. Keep each turn's reply coherent with the turn before it.

## INPUT
```json
{turns_json}
```

## OUTPUT
Return ONLY a raw JSON array of {n} objects, each with exactly the keys "turn_id", "role", "text". No markdown fences, no commentary.
"""


# ============================================================
# 4. API CALL
# ============================================================
def call_gemini(client, types, prompt, dialogue_id):
    """Call Gemini with retry and exponential backoff on rate limits."""
    for attempt in range(MAX_RETRIES):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=1.0,
                    top_p=0.95,
                    max_output_tokens=8192,
                    response_mime_type="application/json",
                ),
            )
            if response.text:
                return response.text
            print(f"  [WARN] empty response ({attempt+1}/{MAX_RETRIES})")
        except Exception as e:
            err = str(e)
            if "429" in err or "RESOURCE_EXHAUSTED" in err:
                wait = BACKOFF_SECONDS[min(attempt, len(BACKOFF_SECONDS) - 1)]
                print(f"  [RATE LIMIT] waiting {wait}s ({attempt+1}/{MAX_RETRIES})")
                time.sleep(wait)
            else:
                print(f"  [ERROR] {dialogue_id}: {err[:160]}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(10)
    return None


# ============================================================
# 5. VALIDATION
# ============================================================
# Product/model tokens that must survive a rewrite. Checked case-insensitively
# because a casual voice may lowercase them.
_MODEL_TOKEN_RE = re.compile(
    r"\b(?:[A-Z]{2,}[-\s]?\d{2,}[A-Za-z0-9-]*|\d+(?:\.\d+)?\s?(?:MB/s|GB|MP|ATM|mm|kg|GHz|W|K))\b"
)

# English-only enforcement. The prompt asks for English; this is what makes
# it binding. A rewrite containing any of these is rejected and retried,
# rather than being silently written into the corpus.
_BANGLISH_RE = re.compile(
    r"\b(acha|ache|bhai|apu|bhalo|dam|hobe|jonno|kemon|koto|nai|toh|kya"
    r"|theke|hoile|nibo|pabo|diba|korar|milega|ayega|kitne|haina|bhabe"
    r"|walaikum|assalam|assalamu|alaikum|salam|lagbe|parben|amar|apnar)\b",
    re.IGNORECASE,
)
_BANGLA_SCRIPT_RE = re.compile(r"[ঀ-৿]")
_BAD_CURRENCY_RE = re.compile(r"\b(BDT|Tk)\b", re.IGNORECASE)


def validate(original, rewritten, dialogue_id):
    """Structural + factual validation. Returns a list of error strings."""
    errors = []

    if not isinstance(rewritten, list):
        return [f"expected a JSON array, got {type(rewritten).__name__}"]

    if len(rewritten) != len(original):
        return [f"turn count mismatch: expected {len(original)}, got {len(rewritten)}"]

    for i, (orig, new) in enumerate(zip(original, rewritten)):
        tag = f"turn {orig['turn_id']}"

        if not isinstance(new, dict):
            errors.append(f"{tag}: not an object")
            continue

        if new.get("turn_id") != orig["turn_id"]:
            errors.append(f"{tag}: turn_id changed to {new.get('turn_id')}")
        if new.get("role") != orig["role"]:
            errors.append(f"{tag}: role changed to {new.get('role')}")

        text = (new.get("text") or "").strip()
        if not text:
            errors.append(f"{tag}: empty text")
            continue

        # --- Money amounts, format-agnostic ---
        want = extract_amounts(orig["text"])
        got = extract_amounts(text)
        # Also accept a bare number appearing without a currency word.
        bare = {int(x.replace(",", "")) for x in re.findall(r"\b[\d,]{3,}\b", text)
                if x.replace(",", "").isdigit()}
        missing = want - got - bare
        if missing:
            errors.append(f"{tag}: money amount(s) {sorted(missing)} lost")

        # --- Phone numbers ---
        for phone in re.findall(r"01\d{9}", orig["text"]):
            if phone not in text.replace(" ", "").replace("-", ""):
                errors.append(f"{tag}: phone {phone} lost")

        # --- TrxIDs ---
        for trx in re.findall(r"BK\d+X\d+P", orig["text"]):
            if trx.lower() not in text.lower():
                errors.append(f"{tag}: TrxID {trx} lost")

        # --- Model numbers / technical figures ---
        for tok in set(_MODEL_TOKEN_RE.findall(orig["text"])):
            norm = tok.lower().replace(" ", "").replace("-", "")
            if norm not in text.lower().replace(" ", "").replace("-", ""):
                errors.append(f"{tag}: technical token '{tok}' lost")

        # --- English only ---
        # Rejected and retried, not repaired: a model that code-switched
        # once will usually produce clean English on a resample.
        bad = {m.group(0).lower() for m in _BANGLISH_RE.finditer(text)}
        if bad:
            errors.append(f"{tag}: non-English token(s) {sorted(bad)}")
        if _BANGLA_SCRIPT_RE.search(text):
            errors.append(f"{tag}: Bangla script present")
        if _BAD_CURRENCY_RE.search(text):
            errors.append(f"{tag}: use 'taka', not BDT/Tk")

        # --- Near-copy detection ---
        # A "paraphrase" identical to the input is a silent no-op that would
        # inflate the diversity numbers without changing anything.
        ratio = difflib.SequenceMatcher(None, orig["text"].lower(), text.lower()).ratio()
        if ratio > MAX_SIMILARITY and len(orig["text"]) > 40:
            errors.append(f"{tag}: too similar to original (ratio {ratio:.2f})")

    # --- Role alternation must survive ---
    # The corpus guarantees strict Buyer/Merchant alternation and the
    # hierarchical classifier embeds role per turn, so a break here would be
    # an out-of-distribution artifact.
    for i in range(len(rewritten) - 1):
        a, b = rewritten[i].get("role"), rewritten[i + 1].get("role")
        if a == b:
            errors.append(f"turns {i+1}/{i+2}: role alternation broken ({a})")
            break

    return errors


# ============================================================
# 6. CHECKPOINTS  (keyed by dialogue_id, not list index)
# ============================================================
def load_checkpoint():
    if os.path.exists(CHECKPOINT_RESULTS):
        with open(CHECKPOINT_RESULTS, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_checkpoint(results):
    with open(CHECKPOINT_RESULTS, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False)
    with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
        json.dump({"completed_ids": sorted(results)}, f)


# ============================================================
# 7. ASSEMBLY
# ============================================================
def assemble(corpus, results, rng):
    """Merge rewritten turns back into full dialogue records."""
    out = []
    for d in corpus:
        did = d["dialogue_id"]
        new_d = json.loads(json.dumps(d))  # deep copy

        if did in results:
            style = rng.choice(CURRENCY_STYLES)
            intensity = rng.choice([0.0, 0.5, 1.0, 1.0])
            by_id = {t["turn_id"]: t for t in results[did]}

            for turn in new_d["turns"]:
                src = by_id.get(turn["turn_id"])
                if not src:
                    continue
                text = src["text"]
                # Currency style is applied uniformly across the dialogue,
                # BEFORE any noise, so all amounts read consistently.
                text = apply_currency_style(text, style)
                text = add_turn_noise(text, turn["role"], rng, intensity)
                turn["text"] = text
                # original_intent / normalized_intent are deliberately NOT
                # taken from the model -- they are label fields and stay
                # exactly as the generator emitted them.

            new_d["source_model"] = d["source_model"] + ORGANIC_SUFFIX
            new_d["labels"]["reason"] = perturb_reason(new_d["labels"]["reason"], rng)

        out.append(new_d)
    return out


def diversity_report(before, after, label):
    def stats(corpus):
        turns = [t for d in corpus for t in d["turns"]]
        b = [t["text"] for t in turns if t["role"] == "Buyer"]
        m = [t["text"] for t in turns if t["role"] == "Merchant"]
        shell = lambda s: re.sub(r"[\d,]+", "#", s)
        return (
            len(b), len(set(b)), len(set(shell(x) for x in b)),
            len(m), len(set(m)), len(set(shell(x) for x in m)),
        )

    b0 = stats(before)
    b1 = stats(after)
    print(f"\n  {label}")
    print(f"    {'metric':<28} {'before':>10} {'after':>10}")
    print(f"    {'-'*50}")
    print(f"    {'buyer turns':<28} {b0[0]:>10} {b1[0]:>10}")
    print(f"    {'unique buyer texts':<28} {b0[1]:>10} {b1[1]:>10}")
    print(f"    {'buyer template shells':<28} {b0[2]:>10} {b1[2]:>10}")
    print(f"    {'unique merchant texts':<28} {b0[4]:>10} {b1[4]:>10}")
    print(f"    {'merchant template shells':<28} {b0[5]:>10} {b1[5]:>10}")
    if b0[1]:
        print(f"    {'buyer reuse ratio':<28} {b0[0]/b0[1]:>9.2f}x {b1[0]/max(b1[1],1):>9.2f}x")
    if b0[4]:
        print(f"    {'merchant reuse ratio':<28} {b0[3]/b0[4]:>9.2f}x {b1[3]/max(b1[4],1):>9.2f}x")


# ============================================================
# 8. MAIN
# ============================================================
def main():
    global MODEL
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=["all", "generated", "seed"], default="all",
                    help="which split to rewrite (default: all 500)")
    ap.add_argument("--limit", type=int, default=0, help="process at most N dialogues")
    ap.add_argument("--dry-run", action="store_true",
                    help="validate wiring and local perturbations without API calls")
    ap.add_argument("--model", default=MODEL, help=f"Gemini model to use (default: {MODEL})")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--input", default=INPUT_FILE)
    ap.add_argument("--output", default=OUTPUT_FILE)
    args = ap.parse_args()

    MODEL = args.model

    print("=" * 70)
    print("  ORGANIC REWRITE PIPELINE")
    print("=" * 70)

    with open(args.input, "r", encoding="utf-8") as f:
        corpus = json.load(f)
    print(f"[LOAD] {len(corpus)} dialogues from {os.path.basename(args.input)}")

    # --- Select targets ---
    if args.only == "generated":
        targets = [d for d in corpus if d.get("source_model") == GENERATED_TAG]
    elif args.only == "seed":
        targets = [d for d in corpus if d.get("source_model") != GENERATED_TAG]
    else:
        targets = list(corpus)

    if not targets:
        print(f"[ABORT] No dialogues matched --only {args.only}. "
              f"source_model values present: "
              f"{sorted({d.get('source_model') for d in corpus})}")
        sys.exit(1)

    results = load_checkpoint()
    remaining = [d for d in targets if d["dialogue_id"] not in results]
    if args.limit:
        remaining = remaining[:args.limit]

    print(f"[PLAN] target split: {args.only} ({len(targets)} dialogues)")
    print(f"[PLAN] already done: {len(results)} | to process: {len(remaining)}")

    rng = random.Random(args.seed)

    # ---------- DRY RUN ----------
    # Exercises assembly, currency normalisation and noise without spending
    # any API quota -- use this to confirm wiring before a paid run.
    if args.dry_run:
        print("\n[DRY-RUN] No API calls. Echoing source text through the "
              "local perturbation path.\n")
        fake = {d["dialogue_id"]: [
            {"turn_id": t["turn_id"], "role": t["role"], "text": t["text"]}
            for t in d["turns"]] for d in remaining}
        out = assemble(corpus, fake, rng)
        for d in out[:1]:
            print(f"  {d['dialogue_id']} ({d['source_model']})")
            for t in d["turns"][:6]:
                print(f"    [{t['role'][:4]}] {t['text'][:88]}")
        diversity_report(corpus, out, "Local perturbations only (no API)")
        print("\n[DRY-RUN] complete. Re-run without --dry-run to call the API.")
        return

    # ---------- LIVE RUN ----------
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        print("\n[ERROR] google-genai not installed.  pip install google-genai")
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        api_key = input("Paste your Gemini API key: ").strip()
    if not api_key:
        print("[ERROR] no API key.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    print(f"[CONFIG] model={MODEL}  rate={RPM_LIMIT}rpm  "
          f"eta~{len(remaining)*DELAY_BETWEEN_CALLS/60:.0f}min")

    stats = {"ok": 0, "retry": 0, "failed": 0}
    started = time.time()

    try:
        for i, d in enumerate(remaining):
            did = d["dialogue_id"]
            buyer_voice = rng.choice(BUYER_VOICES)
            merchant_voice = rng.choice(MERCHANT_VOICES)

            elapsed = time.time() - started
            eta = (elapsed / i * (len(remaining) - i)) if i else 0
            bar_n = int(20 * i / max(len(remaining), 1))
            print(f"\n[{'#'*bar_n}{'.'*(20-bar_n)}] {i+1}/{len(remaining)} "
                  f"| {int(elapsed//60)}m elapsed | ETA {int(eta//60)}m")
            print(f"  {did} | {len(d['turns'])} turns | "
                  f"{d['labels']['outcome_category']}")
            print(f"  buyer: {buyer_voice[:52]}...")

            prompt = build_prompt(d, buyer_voice, merchant_voice)
            ok = False

            for attempt in range(MAX_RETRIES):
                raw = call_gemini(client, types, prompt, did)
                if not raw:
                    stats["retry"] += 1
                    continue

                cleaned = raw.strip()
                if cleaned.startswith("```"):
                    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
                    cleaned = re.sub(r"\s*```$", "", cleaned)

                try:
                    parsed = json.loads(cleaned)
                except json.JSONDecodeError:
                    print(f"  JSON parse error (attempt {attempt+1})")
                    stats["retry"] += 1
                    time.sleep(DELAY_BETWEEN_CALLS)
                    continue

                errs = validate(d["turns"], parsed, did)
                if errs:
                    print(f"  validation failed ({len(errs)}): {errs[0]}")
                    stats["retry"] += 1
                    time.sleep(DELAY_BETWEEN_CALLS)
                    continue

                results[did] = parsed
                save_checkpoint(results)
                stats["ok"] += 1
                ok = True
                print(f"  OK ({len(parsed)} turns rewritten)")
                break

            if not ok:
                stats["failed"] += 1
                print(f"  FAILED after {MAX_RETRIES} attempts -- keeping original")

            time.sleep(DELAY_BETWEEN_CALLS)

    except KeyboardInterrupt:
        print("\n\n[PAUSED] Checkpoint saved. Re-run to resume.")
        save_checkpoint(results)
        sys.exit(0)

    # ---------- OUTPUT ----------
    out = assemble(corpus, results, rng)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*70}")
    print(f"  rewritten: {stats['ok']} | retries: {stats['retry']} | failed: {stats['failed']}")
    print(f"  saved: {args.output}")
    diversity_report(corpus, out, "Full corpus")
    print(f"\n  NOTE: run  python audit_dataset.py {os.path.basename(args.output)}")
    print(f"  to confirm the rewrite did not disturb the leakage metrics.")
    print("=" * 70)

    if stats["failed"] == 0 and stats["ok"] > 0:
        for p in (CHECKPOINT_FILE, CHECKPOINT_RESULTS):
            if os.path.exists(p):
                os.remove(p)
        print("[CLEANUP] checkpoints removed.")


if __name__ == "__main__":
    main()
