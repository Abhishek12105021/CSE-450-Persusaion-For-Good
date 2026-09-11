# Extended Dataset — 500 English Buyer-Seller Intention Dialogues (v2 Compositional)

Corpus file: [`extended_dataset.json`](extended_dataset.json) (structural source of truth)
Training file: [`extended_dataset_organic.json`](extended_dataset_organic.json) (rewritten + English-only — **use this one**)
Generator: [`build_advanced_dialogues.py`](build_advanced_dialogues.py)
Rewrite pass: [`paraphase_pipeline.py`](paraphase_pipeline.py)
English/currency pass: [`enforce_english.py`](enforce_english.py)
Audit tool: [`audit_dataset.py`](audit_dataset.py)

> **Language policy: English only.** No Bangla script, no Banglish or
> romanised Bangla, no Hindi/Urdu — not even single words or greetings. All
> money is written as `32,000 taka`; `BDT` and `Tk` do not appear. This is
> enforced in three places: the rewrite prompt asks for it, the rewrite
> *validator rejects* violations, and [`enforce_english.py`](enforce_english.py)
> re-checks the written corpus and exits non-zero on any residual.

This corpus is the generic-framework counterpart to the donation-intent work in
[`../Intention/`](../Intention/). It is intended for fine-tuning dialogue-level
intent classifiers, so the headline concern is **not** raw size — it is whether
the labels can be predicted without reading the conversation.

---

## 1. Summary

| Metric | Value |
| :--- | :--- |
| Total dialogues | **500** (155 LLM-authored seed + 345 generated) |
| Total turns | **7,953** |
| Buyer / Merchant turns | 4,006 / 3,947 (balanced, strict alternation) |
| Mean turns per dialogue | **15.9** (range 6–32) |
| Products | 40 across 14 categories |
| Buyer archetypes (generated) | 10 |
| `normalized_intent` tags | 16 |
| `original_intent` tags | 483 |
| Language | English only (no Bangla/Banglish; money as `taka`) |
| Organic rewrite coverage | 340 / 500 dialogues |

**Outcome distribution**

| Outcome | Count | `buying_intent` |
| :--- | ---: | :--- |
| PURCHASE_COMMITTED | 238 | yes |
| DEFERRED_CONSIDERATION | 139 | no |
| INQUIRY_DROPOUT | 112 | no |
| EXPLICIT_REJECTION | 11 | no |

Binary balance is 238 `yes` / 262 `no` — near-even, so a majority-class
classifier scores only 52.4%.

---

## 2. Why v1 was rebuilt

The previous generator (`antigravity-advanced-state-machine`) produced 345
dialogues from a **fixed phase pipeline**: greeting → condition → specs → price
→ discount → delivery → advance → close, with the outcome deciding only where
the script stopped. That made the label recoverable from surface features
alone:

| Leakage probe (5-fold holdout) | v1 generated | Seed baseline | **v2 generated** |
| :--- | ---: | ---: | ---: |
| Majority-class baseline | 47.8% | 47.1% | 47.8% |
| Outcome from `turn_count` **alone** | **87.5%** | 63.2% | **48.7%** |
| Outcome from last intent alone | **97.1%** | 83.9% | **75.4%** |
| Unique intent paths | **10 / 345** | 115 / 155 | **318 / 345** |
| Buyer text reuse | 4.20× | 1.02× | 3.40× |
| Merchant text reuse | 4.91× | 1.04× | 2.49× |
| Merchant template shells | 80 (for 3,122 turns) | 629 | 769 |
| Turns carrying `original_intent` | **0 / 6,244** | 1,407 / 1,407 | **6,546 / 6,546** |

In v1, `turn_count` was very nearly the label: 24 turns always meant
`PURCHASE_COMMITTED`, 10 or 16 turns always meant `INQUIRY_DROPOUT`. A model
evaluated on that corpus could score ~90% by counting turns and never reading a
word — it would measure the generator, not the model.

In v2, `turn_count` gives **48.7%** against a 47.8% baseline: length now carries
essentially zero label information, and all four outcomes span overlapping
ranges (dropouts 6–26, commits 8–32).

> **Why paraphrasing was not the fix.** `paraphase_pipeline.py` rewrites turn
> `text` while its validator explicitly pins `turn_id`, `role`, and
> `normalized_intent`. It therefore cannot change `turn_count`, the intent
> sequence, or the phase path — and measurement confirms it: after a 340-dialogue
> run, both `turn_count` and last-intent accuracy are unchanged to the decimal
> (§6). Paraphrasing addresses wording; the v1 defect was structural, and it was
> never the thing standing between v1 and a trainable dataset. It does, however,
> fix the *fourth* leakage row — last-turn template, 77.0% → 51.4% — which is a
> wording problem, and that is worth having.

---

## 3. How v2 generates dialogues

**Compositional phases, not a pipeline.** Optional phases (small talk, variant,
stock re-check, condition, warranty, proof, compare, bulk, urgent) are each
sampled independently, then shuffled. The spec block is inserted at a random
position, and ~28% of buyers ask price *before* discovery. This yields 318
distinct intent paths from 345 dialogues, against v1's 10.

**Archetypes drive phase probability.** A `Skeptic` asks for proof 85% of the
time and re-checks stock 50%; a `LowBaller` negotiates up to 3 rounds; a
`BulkBuyer` almost always asks bulk pricing. Ten archetypes are sampled by
weight, mirroring the seed corpus's persona spread.

**Length decoupled from outcome.** Every outcome exits at several different
phases, each with its own closing. ~22% of committed purchases are "decisive"
buyers who skip discovery entirely and close in 8–12 turns, pushing commits down
into the same length band as dropouts.

**Shared ambiguous closings.** Dropout and deferral draw their final turns from
a common bank (`AMBIGUOUS_BUYER_CLOSE` / `AMBIGUOUS_SELLER_CLOSE`) 45–65% of the
time. Eight closing shells are genuinely label-ambiguous, covering 109
dialogues — a classifier cannot resolve them from the last turn and must use the
dialogue body.

### Known residual — largely resolved by the rewrite

In `extended_dataset.json`, `outcome from last-turn template` sits at **89.6%**
vs the seed's 49.0%. This is concentrated in `PURCHASE_COMMITTED`, which
legitimately ends with an order confirmation ("Payment received and verified…").
Some of that is genuine signal — a confirmed transaction really does look
different at the last turn, in the seed corpus too — but 89.6% was mostly the
generator reusing a small bank of closing templates.

The organic rewrite (§6) brings this to **53.0%** on the generated split against
a 47.8% baseline, which is the level the seed corpus shows. **This is the main
reason to train on `extended_dataset_organic.json` rather than
`extended_dataset.json`.** The dropout/deferral boundary, which is the hard and
interesting one, remains deliberately ambiguous in both.

---

## 4. Schema

Every dialogue, seed and generated, carries identical keys:

```json
{
  "dialogue_id": "ENG_290",
  "source_file": "compositional_generator_v2.json",
  "source_model": "compositional-generator-v2-organic",
  "original_id": 135,
  "product": "Sony WH-1000XM5 Wireless Headphones",
  "category": "Audio & Visual Gear",
  "archetype": "Skeptic",
  "language_style": "Pure English",
  "labels": {
    "buying_intent": "yes",
    "outcome_category": "PURCHASE_COMMITTED",
    "reason": "Buyer completed negotiation, accepted advance policy, and committed to purchase."
  },
  "turn_count": 10,
  "turns": [
    {
      "role": "Buyer",
      "text": "Hi there! I was hoping to grab a pair of Sony WH-1000XM5 Wireless Headphones. Do you happen to have them in stock?",
      "original_intent": "ASK_AVAILABILITY",
      "normalized_intent": "INQUIRE_INFO",
      "turn_id": 1
    }
  ]
}
```

Verified invariants (all 500 dialogues):

- unique `dialogue_id`; `turn_count == len(turns)`; `turn_id` is exactly `1..n`
- strict Buyer/Merchant alternation, always opening on Buyer (matches seed)
- `buying_intent == "yes"` **iff** `outcome_category == "PURCHASE_COMMITTED"`
- no empty turn text; no Unicode replacement characters
- every turn has both `original_intent` and `normalized_intent`
- English only; no `BDT`/`Tk`; the only non-ASCII character is `°`

In `extended_dataset_organic.json`, rewritten dialogues carry an `-organic`
suffix on `source_model` (`claude-organic`, `compositional-generator-v2-organic`).
Strip that suffix before comparing against seed/generated tags — `audit_dataset.py`
does.

The alternation invariant matters for [`../Intention/Classifier/`](../Intention/Classifier/):
the hierarchical model (v6/v8) adds a **per-turn role embedding**, so a doubled
speaker would be an out-of-distribution artifact. When two composed phases would
both emit the same speaker, `DialogueBuilder.add()` merges them into one turn —
as a real chat participant sending two thoughts in one message.

---

## 5. Usage

```bash
# Regenerate (default: 345 dialogues, seed 104)
python build_advanced_dialogues.py --n 345 --seed 104

# Audit any corpus for leakage before training
python audit_dataset.py extended_dataset.json extended_dataset_organic.json

# Confirm the English-only / currency invariants still hold
python enforce_english.py --verify-only extended_dataset_organic.json
```

Run the audit **before every fine-tuning run** and compare the generated split
against the seed baseline. If `turn_count` or last-intent accuracy drifts far
above the seed column, the generator has reintroduced a shortcut and the
resulting eval numbers will be inflated.

### Converting to the `Intention/` CSV format

The classifiers there read a dialogue-level CSV with `[Persuader]` /
`[Persuadee]` speaker markers. Merchant maps to Persuader (the persuading
party), Buyer to Persuadee (the deciding party), and `buying_intent` is already
the `yes`/`no` binary label:

```python
import json, csv
d = json.load(open("extended_dataset_organic.json", encoding="utf-8"))
role = {"Merchant": "[Persuader]", "Buyer": "[Persuadee]"}
with open("generic_manual_label.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["conversation_id", "dialogue_id", "dialogue_text", "binary_label"])
    for i, x in enumerate(d):
        text = "\r\n ".join(f"{role[t['role']]} {t['text']}" for t in x["turns"])
        w.writerow([i, x["dialogue_id"], text, x["labels"]["buying_intent"]])
```

---

## 6. Organic rewrite pass

`paraphase_pipeline.py` rewrites turn *wording* via the Gemini API so the text
reads like real Facebook-page chat — typos, lowercase, dropped punctuation,
split messages — without touching any structural or label field.

```bash
python paraphase_pipeline.py --dry-run --limit 5   # verify wiring, no API calls
python paraphase_pipeline.py                       # all 500 dialogues
python enforce_english.py                          # English-only + currency
python audit_dataset.py extended_dataset_organic.json
```

It writes to `extended_dataset_organic.json` and leaves `extended_dataset.json`
untouched, so the structural corpus stays the source of truth.

**Run it only on a corpus that already passes the audit.** It is a polish pass;
it cannot repair structural leakage (see §2).

### Measured result

The rewrite pass has been run over **340 of 500 dialogues** (146 seed, 194
generated); the remaining 160 keep their generator text. Re-running resumes
from the checkpoint. Full corpus, before vs after:

| Full corpus | before | after |
| :--- | ---: | ---: |
| outcome from `turn_count` | 49.0% | 49.0% |
| outcome from last intent | 78.8% | 78.8% |
| **outcome from last-turn template** | **77.0%** | **51.4%** |
| buyer text reuse | 2.38× | **1.33×** |
| merchant text reuse | 2.01× | **1.26×** |
| buyer template shells | 1,237 / 4,006 | **2,741 / 4,006** |
| merchant template shells | 1,398 / 3,947 | **2,766 / 3,947** |

The last-turn-template row is the point of the exercise. §3 previously recorded
**89.6%** on the generated split as a "known, intentional residual"; the rewrite
brings it to **53.0%** against a 47.8% baseline — roughly 5 points of genuine
end-of-transaction signal instead of 42 points of template fingerprint. The two
rows that did not move cannot move: the validator pins `turn_count` and the
intent sequence by design (see §2).

On the 340 rewritten dialogues in isolation, text reuse is effectively
eliminated — **1.02× buyer / 1.00× merchant**, matching the seed baseline.
Median turn-level similarity to the source is 0.52, and only 7 of 4,499
rewritten turns (0.2%) came back near-identical, so the near-copy validator is
doing real work.

### English-only enforcement

The rewrite alone did not deliver a clean English corpus: it left 254 Banglish
tokens, 5 turns of literal Bangla script, and four competing currency spellings.
`enforce_english.py` closes that gap and is idempotent — `--verify-only` exits
non-zero if anything is left.

| | before | after |
| :--- | ---: | ---: |
| Banglish tokens | 254 | **0** |
| `BDT` / `Tk` mentions | 1,998 | **0** |
| Bangla-script turns | 5 | **0** |
| non-ASCII turns | 149 | **1** (a `°` in "350 degrees") |

It rewrote 1,867 turns across 370 dialogues and changed **nothing else** — the
script aborts without writing if turn counts, turn_ids, roles, intents, labels,
or any digit in any turn differ from the input. The leakage table above is
measured *after* this pass and is identical to before it.

Three upstream sources of the contamination are now fixed, so a re-run cannot
reintroduce it:

- `FILLERS_BUYER` contained `"acha "`, which injected Banglish into turns the
  API had already returned as clean English (45 occurrences).
- `CURRENCY_STYLES` offered four spellings; it is now `["taka"]` only.
- The prompt's English-only request is now **hard rule 0**, and — since a prompt
  rule is only a request — the validator rejects and retries any turn containing
  Banglish, Bangla script, or `BDT`/`Tk`.

Two latent bugs were fixed alongside: a missing comma in `BUYER_VOICES` silently
concatenated two personas into one malformed string, and a merchant voice entry
had a stray instruction fragment glued onto it.

### What the pass guarantees

- **Wording changes, labels do not.** `normalized_intent` and `original_intent`
  are re-attached from the source turn and never taken from the model, so a bad
  generation cannot corrupt a label.
- **One voice per dialogue.** Buyer and merchant voices are sampled per
  conversation, not per turn.
- **One currency word corpus-wide.** `32,000 taka`, everywhere.
- **Thirteen validated failure modes.** Turn count, turn order, role, role
  alternation, empty text, lost money amounts (format-agnostic), lost phone
  numbers, lost TrxIDs, lost model/spec tokens, near-copy no-ops, Banglish
  tokens, Bangla script, and wrong currency word.
- **Resume by `dialogue_id`.** Checkpoints key on id rather than list index, so
  resuming after a regeneration cannot mis-assign results.

Bugs fixed from earlier versions, worth knowing if you have old output:

1. It filtered on `antigravity-advanced-state-machine`, a `source_model` tag no
   longer present — it would have matched **0 dialogues** and written an
   unchanged file with success messaging. The pipeline now aborts loudly and
   prints the tags actually present.
2. `perturb_price_format` ran *after* validation and re-randomised each amount
   independently, so a validated dialogue could be written out saying
   `32,000 BDT` in one turn and `BDT 32,000` in the next — and the old validator
   regex could not match the prefix form at all, making the corruption invisible
   on a re-run. Moot now that there is one currency style, but the ordering fix
   stands.
3. The prompt requested only four keys, silently dropping `original_intent` from
   every rewritten turn — reintroducing the exact schema break §2 lists as a v1
   defect.
4. `perturb_reason`'s lookup table was keyed on v1 reason strings and matched
   none of the 13 reasons the v2 generator emits.
5. `audit_dataset.py` compared `source_model` against `SEED_MODELS` by exact
   match, but the rewrite appends `-organic`. Auditing the organic file put 146
   seed dialogues in the GENERATED bucket and printed a nonsense 9-dialogue
   SEED group. It now strips the suffix before the membership test — **re-audit
   any organic corpus you scored before this fix.**

---

## 7. Label semantics vs. `Intention/`

Note the label-semantics difference from `Intention/`: there, `binary_label`
requires a *fully unconditional* commitment, and any hedge makes it `no`. Here,
`PURCHASE_COMMITTED` means the buyer confirmed the order and sent payment
details, while every hedged or deferred ending is already `no` — the two schemes
agree in spirit, but do not transfer a trained model without re-checking the
boundary cases.
