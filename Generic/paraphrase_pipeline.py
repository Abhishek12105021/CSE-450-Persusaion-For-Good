"""
Paraphrase Pipeline for Buyer-Seller Dialogue Dataset
======================================================
Diversifies the 345 procedurally-generated state-machine dialogues
using the Gemini API (gemini-2.0-flash-lite) with:
  - Style-randomized whole-dialogue paraphrasing
  - Local perturbations (price format, fillers, reason text)
  - Checkpoint/resume support
  - Strict structural validation
  - Rate limiting with exponential backoff

Usage:
    set GEMINI_API_KEY=your_api_key_here
    python paraphrase_pipeline.py

    Or run directly and paste your key when prompted.
"""

import os
import sys
import json
import time
import random
import re
from collections import Counter

from google import genai
from google.genai import types

# ============================================================
# 1. CONFIGURATION
# ============================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL = "gemini-2.0-flash-lite"       # Swap if your AI Studio shows a different name
RPM_LIMIT = 10                         # Requests per minute (safe under ~15 RPM free cap)
DELAY_BETWEEN_CALLS = 60.0 / RPM_LIMIT  # = 6 seconds

INPUT_FILE = os.path.join(SCRIPT_DIR, "extended_dataset.json")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "extended_dataset_paraphrased.json")
CHECKPOINT_FILE = os.path.join(SCRIPT_DIR, "paraphrase_checkpoint.json")

MAX_RETRIES = 3
BACKOFF_SECONDS = [30, 60, 120]  # Exponential backoff on 429 errors

# Filter: only paraphrase state-machine generated dialogues
SOURCE_MODEL_TAG = "antigravity-advanced-state-machine"
PARAPHRASED_TAG = "antigravity-advanced-state-machine-paraphrased"

# ============================================================
# 2. STYLE RANDOMIZER
# ============================================================
PARAPHRASE_STYLES = [
    "casual and conversational, like texting a friend — use contractions, informal language, and occasional short forms",
    "formal and polite — use complete sentences, courteous language, and professional tone",
    "hurried and brief — use short, clipped sentences as if the person is busy and typing quickly",
    "friendly and chatty — use warm, enthusiastic language with filler words like 'actually', 'honestly', 'you know'",
    "minimalist — use the fewest words possible while keeping the meaning clear, no pleasantries",
    "slightly hesitant — use hedging language like 'I think', 'maybe', 'not sure but', 'I was wondering'",
    "direct and assertive — use confident, straightforward language without hedging or excessive politeness",
    "curious and detail-oriented — ask follow-up nuances, use phrases like 'just to clarify', 'one more thing'",
    "neutral and matter-of-fact — standard conversational English, no strong emotional tone in either direction",
    "warm but pragmatic — polite and friendly but focused on getting the deal done efficiently",
]

# ============================================================
# 3. LOCAL PERTURBATIONS (No API needed)
# ============================================================
def perturb_price_format(text):
    """Randomly vary how BDT prices are displayed in the text."""
    def replace_price(match):
        raw = match.group(0)
        # Extract the numeric part
        num_str = re.sub(r'[^\d]', '', raw.split('BDT')[0].split('Tk')[0].split('taka')[0].strip())
        if not num_str:
            return raw
        num = int(num_str)
        
        formats = [
            f"{num:,} BDT",
            f"BDT {num:,}",
            f"{num:,} Tk",
            f"{num:,} taka",
            f"{num} BDT",
        ]
        return random.choice(formats)
    
    # Match patterns like "32,000 BDT", "BDT 32,000", etc.
    result = re.sub(r'(?:BDT\s*)?[\d,]+\s*(?:BDT|Tk|taka)', replace_price, text, flags=re.IGNORECASE)
    return result


def perturb_reason(reason):
    """Slightly vary the labels.reason text for diversity."""
    variations = {
        "Buyer completed negotiation, accepted advance policy, and committed to purchase.": [
            "Buyer successfully negotiated, agreed to the advance payment policy, and finalized the purchase.",
            "After negotiation and accepting the advance fee, the buyer committed to buying.",
            "The buyer went through price negotiation, accepted the advance requirement, and completed the order.",
            "Buyer negotiated the price, agreed to pay the advance, and confirmed the purchase.",
            "Purchase was committed after the buyer accepted the negotiated price and advance policy.",
        ],
        "Buyer deferred decision after learning the price and specs.": [
            "Buyer chose to delay the purchase decision after reviewing price and specifications.",
            "After hearing the price and specs, the buyer decided to think it over.",
            "The buyer postponed their decision upon learning the price and product details.",
            "Buyer asked for time to consider after receiving pricing and specification information.",
            "Decision was deferred by the buyer after the price and specs were discussed.",
        ],
        "Buyer abandoned dialogue after merchant refused discount.": [
            "The buyer left after the merchant wouldn't lower the price.",
            "Buyer dropped out when the discount request was denied by the merchant.",
            "After the merchant refused to negotiate on price, the buyer walked away.",
            "The buyer abandoned the conversation following the merchant's discount refusal.",
            "Buyer exited the negotiation after their discount request was rejected.",
        ],
        "Buyer dropped out early due to technical specification mismatch.": [
            "The buyer left early because the specs didn't match their requirements.",
            "A technical specification mismatch caused the buyer to drop out early.",
            "Buyer abandoned the inquiry early after finding the specs unsuitable.",
            "The buyer exited early — the product's technical specs didn't meet their needs.",
            "Early dropout by buyer due to a mismatch in desired technical specifications.",
        ],
        "Buyer explicitly rejected mandatory advance fee and walked away.": [
            "The buyer refused to pay the mandatory advance and cancelled.",
            "Buyer rejected the advance payment policy outright and left.",
            "The buyer explicitly declined the advance fee requirement and walked away.",
            "Buyer refused the mandatory advance deposit and terminated the conversation.",
            "The advance fee policy was explicitly rejected by the buyer, ending the dialogue.",
        ],
    }
    if reason in variations:
        return random.choice(variations[reason])
    return reason


# ============================================================
# 4. PROMPT CONSTRUCTION
# ============================================================
def build_prompt(dialogue, style):
    """Build the paraphrase prompt for Gemini."""
    turns_json = json.dumps(dialogue["turns"], indent=2, ensure_ascii=False)
    
    prompt = f"""You are a dialogue paraphrasing assistant. Your task is to rewrite every turn's "text" in the conversation below to sound natural and varied, while strictly preserving all structural and factual information.

## STYLE INSTRUCTION
Rewrite ALL turns (both Buyer and Merchant) in this style: **{style}**

## STRICT RULES
1. **Preserve EXACTLY**: turn_id, role, normalized_intent for every turn — do NOT change these fields.
2. **Preserve ALL factual content**: product names, exact BDT prices/numbers, phone numbers, addresses, TrxIDs, technical specifications (e.g., "8 microphones", "30 hours battery", "1050 MB/s"). These must appear in the paraphrased text.
3. **Change the wording**: Use different sentence structures, vocabulary, synonyms, and phrasing. Do NOT just copy the original text with minor word swaps.
4. **Maintain conversational coherence**: Each turn should naturally follow the previous one. If the buyer asks about a spec, the merchant's answer should still address that spec.
5. **Keep the same number of turns**: Output must have exactly {len(dialogue["turns"])} turns.

## INPUT DIALOGUE
```json
{turns_json}
```

## OUTPUT FORMAT
Return ONLY a valid JSON array of objects. Each object must have exactly these keys: "turn_id", "role", "text", "normalized_intent". No markdown fences, no explanation, just the raw JSON array.
"""
    return prompt


# ============================================================
# 5. API CALL WITH RATE LIMITING & RETRY
# ============================================================
def call_gemini(client, prompt, dialogue_id):
    """Call Gemini API with retry and exponential backoff."""
    for attempt in range(MAX_RETRIES):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.9,
                    top_p=0.95,
                    max_output_tokens=4096,
                    response_mime_type="application/json",
                ),
            )
            
            if response.text:
                return response.text
            else:
                print(f"  [WARN] Empty response for {dialogue_id}, attempt {attempt+1}/{MAX_RETRIES}")
                
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                wait = BACKOFF_SECONDS[min(attempt, len(BACKOFF_SECONDS)-1)]
                print(f"  [RATE LIMIT] 429 on {dialogue_id}, waiting {wait}s (attempt {attempt+1}/{MAX_RETRIES})")
                time.sleep(wait)
            else:
                print(f"  [ERROR] {dialogue_id} attempt {attempt+1}: {error_str[:200]}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(10)
    
    return None


# ============================================================
# 6. RESPONSE VALIDATION
# ============================================================
def validate_response(original_turns, paraphrased_turns, dialogue_id):
    """Validate that the paraphrased response preserves structure and facts."""
    errors = []
    
    # Check turn count
    if len(paraphrased_turns) != len(original_turns):
        errors.append(f"Turn count mismatch: expected {len(original_turns)}, got {len(paraphrased_turns)}")
        return errors  # Fatal — can't check further
    
    for i, (orig, para) in enumerate(zip(original_turns, paraphrased_turns)):
        turn_label = f"turn {orig['turn_id']}"
        
        # Check turn_id preserved
        if para.get("turn_id") != orig["turn_id"]:
            errors.append(f"{turn_label}: turn_id changed from {orig['turn_id']} to {para.get('turn_id')}")
        
        # Check role preserved
        if para.get("role") != orig["role"]:
            errors.append(f"{turn_label}: role changed from {orig['role']} to {para.get('role')}")
        
        # Check normalized_intent preserved
        if para.get("normalized_intent") != orig["normalized_intent"]:
            errors.append(f"{turn_label}: intent changed from {orig['normalized_intent']} to {para.get('normalized_intent')}")
        
        # Check text exists and is non-empty
        if not para.get("text") or not para["text"].strip():
            errors.append(f"{turn_label}: text is empty or missing")
            continue
        
        # Check critical factual tokens are preserved
        # Extract BDT amounts from original
        prices_in_orig = re.findall(r'[\d,]+(?:\s*(?:BDT|Tk|taka))', orig["text"], re.IGNORECASE)
        for price_token in prices_in_orig:
            # Extract just the numeric part for comparison
            num = re.sub(r'[^\d]', '', price_token)
            if num and len(num) >= 3:  # Only check meaningful numbers (not turn_ids etc.)
                if num not in re.sub(r'[^\d\s]', ' ', para["text"]):
                    # Try with commas removed
                    if num not in para["text"].replace(",", ""):
                        errors.append(f"{turn_label}: price number '{num}' missing from paraphrased text")
        
        # Check phone numbers preserved
        phones_in_orig = re.findall(r'01\d{9}', orig["text"])
        for phone in phones_in_orig:
            if phone not in para["text"]:
                errors.append(f"{turn_label}: phone '{phone}' missing from paraphrased text")
        
        # Check TrxID preserved
        trxids = re.findall(r'BK\d+X\d+P', orig["text"])
        for trxid in trxids:
            if trxid not in para["text"]:
                errors.append(f"{turn_label}: TrxID '{trxid}' missing from paraphrased text")
    
    return errors


# ============================================================
# 7. CHECKPOINT MANAGEMENT
# ============================================================
def load_checkpoint():
    """Load checkpoint of completed dialogue indices."""
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return set(data.get("completed_indices", []))
    return set()


def save_checkpoint(completed_indices):
    """Save checkpoint of completed dialogue indices."""
    with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
        json.dump({"completed_indices": sorted(completed_indices)}, f)


# ============================================================
# 8. MAIN PIPELINE
# ============================================================
def main():
    print("=" * 70)
    print("  PARAPHRASE PIPELINE — Gemini API Dialogue Diversifier")
    print("=" * 70)
    
    # --- Get API Key ---
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        print("\nNo GEMINI_API_KEY environment variable found.")
        api_key = input("Paste your Gemini API key here: ").strip()
        if not api_key:
            print("ERROR: No API key provided. Exiting.")
            sys.exit(1)
    
    # --- Initialize Client ---
    client = genai.Client(api_key=api_key)
    print(f"\n[CONFIG] Model: {MODEL}")
    print(f"[CONFIG] Rate limit: {RPM_LIMIT} RPM ({DELAY_BETWEEN_CALLS:.1f}s delay)")
    print(f"[CONFIG] Input: {INPUT_FILE}")
    print(f"[CONFIG] Output: {OUTPUT_FILE}")
    
    # --- Load Dataset ---
    print("\n[LOAD] Reading dataset...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        corpus = json.load(f)
    print(f"[LOAD] Total dialogues: {len(corpus)}")
    
    # Separate seed vs state-machine dialogues (by index)
    seed_indices = []
    sm_indices = []
    for i, d in enumerate(corpus):
        if d.get("source_model") == SOURCE_MODEL_TAG:
            sm_indices.append(i)
        else:
            seed_indices.append(i)
    
    print(f"[LOAD] Seed dialogues (untouched): {len(seed_indices)}")
    print(f"[LOAD] State-machine dialogues (to paraphrase): {len(sm_indices)}")
    
    # --- Pre-run Statistics ---
    sm_buyer_texts = [t["text"] for i in sm_indices for t in corpus[i]["turns"] if t["role"] == "Buyer"]
    unique_before = len(set(sm_buyer_texts))
    reuse_before = len(sm_buyer_texts) / unique_before if unique_before > 0 else 0
    print(f"\n[STATS BEFORE] Buyer turns: {len(sm_buyer_texts)}, Unique texts: {unique_before}, Reuse ratio: {reuse_before:.2f}x")
    
    # --- Load Checkpoint ---
    completed = load_checkpoint()
    remaining = [i for i in sm_indices if i not in completed]
    print(f"\n[CHECKPOINT] Already completed: {len(completed)}, Remaining: {len(remaining)}")
    
    if not remaining:
        print("[DONE] All dialogues already paraphrased! Assembling output...")
    else:
        est_minutes = len(remaining) * DELAY_BETWEEN_CALLS / 60
        print(f"[ESTIMATE] ~{est_minutes:.1f} minutes for {len(remaining)} remaining dialogues")
        print(f"\n{'─' * 70}")
        print(f"  Starting paraphrase pipeline... (Press Ctrl+C to pause safely)")
        print(f"{'─' * 70}\n")
    
    # --- Set random seed for reproducible local perturbations ---
    random.seed(42)
    
    # --- Process Each Dialogue ---
    stats = {"success": 0, "validation_retry": 0, "failed": 0, "skipped_checkpoint": len(completed)}
    pipeline_start_time = time.time()
    paraphrased_results = {}  # index -> paraphrased turns
    
    # Load any previously paraphrased results from checkpoint
    checkpoint_results_file = CHECKPOINT_FILE.replace(".json", "_results.json")
    if os.path.exists(checkpoint_results_file):
        with open(checkpoint_results_file, "r", encoding="utf-8") as f:
            saved_results = json.load(f)
            paraphrased_results = {int(k): v for k, v in saved_results.items()}
    
    try:
        for progress_idx, corpus_idx in enumerate(remaining):
            dialogue = corpus[corpus_idx]
            d_id = dialogue["dialogue_id"]
            
            # Pick a random style
            style = random.choice(PARAPHRASE_STYLES)
            
            # --- Progress bar & time tracking ---
            elapsed = time.time() - pipeline_start_time
            done_count = progress_idx  # completed before this one
            if done_count > 0:
                avg_per_item = elapsed / done_count
                eta_seconds = avg_per_item * (len(remaining) - done_count)
                eta_min, eta_sec = divmod(int(eta_seconds), 60)
                eta_str = f"ETA {eta_min}m {eta_sec}s"
            else:
                eta_str = "ETA calculating..."
            elapsed_min, elapsed_sec = divmod(int(elapsed), 60)
            
            pct = (progress_idx / len(remaining)) * 100
            bar_len = 20
            filled = int(bar_len * progress_idx / len(remaining))
            bar = '█' * filled + '░' * (bar_len - filled)
            
            print(f"\n[{bar}] {pct:5.1f}% | {progress_idx+1}/{len(remaining)} | {elapsed_min}m{elapsed_sec:02d}s elapsed | {eta_str}")
            print(f"  {d_id} | turns: {len(dialogue['turns'])} | outcome: {dialogue['labels']['outcome_category']}")
            print(f"  style: '{style[:60]}...'")
            print(f"  ", end="", flush=True)
            
            # Build prompt
            prompt = build_prompt(dialogue, style)
            
            # Try up to MAX_RETRIES times
            success = False
            for attempt in range(MAX_RETRIES):
                # Call API
                raw_response = call_gemini(client, prompt, d_id)
                
                if not raw_response:
                    print(f"no response (attempt {attempt+1}) ", end="", flush=True)
                    stats["validation_retry"] += 1
                    continue
                
                # Parse JSON
                try:
                    # Clean response — strip markdown fences if present
                    cleaned = raw_response.strip()
                    if cleaned.startswith("```"):
                        cleaned = re.sub(r'^```(?:json)?\s*', '', cleaned)
                        cleaned = re.sub(r'\s*```$', '', cleaned)
                    
                    paraphrased_turns = json.loads(cleaned)
                except json.JSONDecodeError as e:
                    print(f"JSON parse error (attempt {attempt+1}) ", end="", flush=True)
                    stats["validation_retry"] += 1
                    time.sleep(DELAY_BETWEEN_CALLS)
                    continue
                
                # Validate
                errors = validate_response(dialogue["turns"], paraphrased_turns, d_id)
                
                if errors:
                    print(f"validation failed ({len(errors)} errors, attempt {attempt+1}) ", end="", flush=True)
                    if len(errors) <= 3:
                        for err in errors:
                            print(f"\n    └─ {err}", end="")
                    stats["validation_retry"] += 1
                    time.sleep(DELAY_BETWEEN_CALLS)
                    continue
                
                # Success!
                paraphrased_results[corpus_idx] = paraphrased_turns
                completed.add(corpus_idx)
                save_checkpoint(completed)
                
                # Save results incrementally
                with open(checkpoint_results_file, "w", encoding="utf-8") as f:
                    json.dump({str(k): v for k, v in paraphrased_results.items()}, f, ensure_ascii=False)
                
                stats["success"] += 1
                success = True
                print(f"✓ paraphrased ({len(paraphrased_turns)} turns)")
                break
            
            if not success:
                stats["failed"] += 1
                print(f"✗ FAILED after {MAX_RETRIES} attempts")
            
            # --- Periodic summary every 25 dialogues ---
            processed_so_far = progress_idx + 1
            if processed_so_far % 25 == 0:
                elapsed_now = time.time() - pipeline_start_time
                e_min, e_sec = divmod(int(elapsed_now), 60)
                rate = processed_so_far / (elapsed_now / 60) if elapsed_now > 0 else 0
                success_rate = (stats['success'] / processed_so_far * 100) if processed_so_far > 0 else 0
                print(f"\n  {'─' * 60}")
                print(f"  📊 PROGRESS SUMMARY (after {processed_so_far} dialogues)")
                print(f"     Elapsed: {e_min}m {e_sec}s | Rate: {rate:.1f} dialogues/min")
                print(f"     Success: {stats['success']} | Retries: {stats['validation_retry']} | Failed: {stats['failed']}")
                print(f"     Success rate: {success_rate:.1f}%")
                print(f"  {'─' * 60}")
            
            # Rate limit delay
            time.sleep(DELAY_BETWEEN_CALLS)
    
    except KeyboardInterrupt:
        elapsed_total = time.time() - pipeline_start_time
        et_min, et_sec = divmod(int(elapsed_total), 60)
        print(f"\n\n{'=' * 70}")
        print(f"  ⏸️  INTERRUPTED after {et_min}m {et_sec}s")
        print(f"  Completed: {len(completed)} / {len(sm_indices)} dialogues")
        print(f"  Success: {stats['success']} | Retries: {stats['validation_retry']} | Failed: {stats['failed']}")
        print(f"{'=' * 70}")
        print(f"\n[SAVING] Checkpoint...")
        save_checkpoint(completed)
        with open(checkpoint_results_file, "w", encoding="utf-8") as f:
            json.dump({str(k): v for k, v in paraphrased_results.items()}, f, ensure_ascii=False)
        print(f"[SAVED] Run 'python paraphrase_pipeline.py' again to resume from dialogue #{len(completed)+1}.")
        sys.exit(0)
    
    # --- Assemble Output ---
    print(f"\n{'=' * 70}")
    print(f"  ASSEMBLING OUTPUT")
    print(f"{'=' * 70}")
    
    output_corpus = []
    for i, dialogue in enumerate(corpus):
        if i in paraphrased_results:
            # Use paraphrased version
            new_dialogue = json.loads(json.dumps(dialogue))  # deep copy
            new_dialogue["turns"] = paraphrased_results[i]
            new_dialogue["source_model"] = PARAPHRASED_TAG
            
            # Apply local perturbations
            new_dialogue["labels"]["reason"] = perturb_reason(new_dialogue["labels"]["reason"])
            
            # Apply price format perturbation to all turns
            for turn in new_dialogue["turns"]:
                turn["text"] = perturb_price_format(turn["text"])
            
            output_corpus.append(new_dialogue)
        else:
            # Keep original (seed dialogues or failed paraphrases)
            output_corpus.append(dialogue)
    
    # --- Save Output ---
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output_corpus, f, indent=2, ensure_ascii=False)
    print(f"\n[SAVED] {OUTPUT_FILE}")
    
    # --- Post-Run Statistics ---
    print(f"\n{'=' * 70}")
    print(f"  POST-RUN STATISTICS")
    print(f"{'=' * 70}")
    
    print(f"\n  Pipeline Results:")
    print(f"    Successful paraphrases: {stats['success']}")
    print(f"    Skipped (from checkpoint): {stats['skipped_checkpoint']}")
    print(f"    Validation retries: {stats['validation_retry']}")
    print(f"    Failed (after all retries): {stats['failed']}")
    
    # Compute diversity metrics on paraphrased state-machine dialogues
    sm_output = [output_corpus[i] for i in sm_indices]
    new_buyer_texts = [t["text"] for d in sm_output for t in d["turns"] if t["role"] == "Buyer"]
    unique_after = len(set(new_buyer_texts))
    reuse_after = len(new_buyer_texts) / unique_after if unique_after > 0 else 0
    
    print(f"\n  Diversity Metrics (state-machine dialogues only):")
    print(f"    {'Metric':<30} {'Before':>10} {'After':>10} {'Change':>10}")
    print(f"    {'─' * 62}")
    print(f"    {'Total buyer turns':<30} {len(sm_buyer_texts):>10} {len(new_buyer_texts):>10} {'—':>10}")
    print(f"    {'Unique buyer texts':<30} {unique_before:>10} {unique_after:>10} {f'+{unique_after - unique_before}':>10}")
    print(f"    {'Text reuse ratio':<30} {f'{reuse_before:.2f}x':>10} {f'{reuse_after:.2f}x':>10} {f'{reuse_after - reuse_before:+.2f}x':>10}")
    
    # Also check merchant diversity
    sm_merchant_before = [t["text"] for i in sm_indices for t in corpus[i]["turns"] if t["role"] == "Merchant"]
    sm_merchant_after = [t["text"] for d in sm_output for t in d["turns"] if t["role"] == "Merchant"]
    unique_m_before = len(set(sm_merchant_before))
    unique_m_after = len(set(sm_merchant_after))
    
    print(f"\n    {'Unique merchant texts':<30} {unique_m_before:>10} {unique_m_after:>10} {f'+{unique_m_after - unique_m_before}':>10}")
    
    # Check overall corpus
    all_buyer = [t["text"] for d in output_corpus for t in d["turns"] if t["role"] == "Buyer"]
    print(f"\n  Full Corpus (500 dialogues):")
    print(f"    Total buyer turns: {len(all_buyer)}")
    print(f"    Unique buyer texts: {len(set(all_buyer))}")
    print(f"    Reuse ratio: {len(all_buyer) / len(set(all_buyer)):.2f}x")
    
    print(f"\n{'=' * 70}")
    print(f"  DONE! Output saved to: {OUTPUT_FILE}")
    print(f"{'=' * 70}")
    
    # Cleanup checkpoint files on full success
    if stats["failed"] == 0 and len(remaining) > 0:
        print("\n[CLEANUP] All dialogues processed successfully. Removing checkpoint files...")
        for f_path in [CHECKPOINT_FILE, checkpoint_results_file]:
            if os.path.exists(f_path):
                os.remove(f_path)
                print(f"  Removed: {f_path}")


if __name__ == "__main__":
    main()
