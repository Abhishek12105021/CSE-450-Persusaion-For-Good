# MAPL Capstone — Donation-Intent Classifier, Architecture v7

This documents `capstone-v7-augmentation-plus.ipynb`, a fork of v5
(`capstone-v5-augfix.ipynb` — see [architecture-v5.md](architecture-v5.md)).
**Model, loss, and training loop are byte-for-byte unchanged from v5**
(confirmed by diffing the two notebooks — only cells 0, 2, 4, 11-14, 28,
40 differ, all in the intro/config/augmentation/reporting-header area).
Only the augmentation step changes.

---

## 1. What prompted this fork

Unlike v3-v6, this one is grounded in actual executed results, not just
code-reading. `ran-nb/ran-v4.ipynb` and `ran-nb/ran-v5.ipynb` contain
cached outputs from real Kaggle runs. Pulled from their classification
reports (test split, all 3 encoders):

| Class | v4 F1 (roberta / deberta-v3 / todbert) | v5 F1 (roberta / deberta-v3 / todbert) |
|---|---|---|
| `conditional` (support=3) | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 |
| `deferred` (support=19) | 0.18 / 0.10 / 0.07 | 0.09 / 0.13 / 0.00 |
| binary macro-F1 | 0.656 / 0.630 / 0.649 | 0.648 / 0.670 / 0.623 |

Two takeaways:

1. **`conditional` F1 is exactly 0.00 in all six runs** (both v4 and v5,
   all three encoders) — precision and recall both 0, meaning the model
   never predicts `conditional` as its argmax on the test set, in any run.
2. **v5's augmentation change didn't consistently help `deferred`** — 2 of
   3 encoders scored lower than their v4 counterpart. Not proof the
   Persuadee-bias change is harmful (n=3 per condition can't separate
   signal from noise), but it's not evidence it helped either.

---

## 2. Root cause

`conditional`'s 63 v5-augmented training copies (and most of `deferred`'s
141) all trace back to ~13 / ~68 real source dialogues. EDA's four
operations (synonym / swap / delete / insert) all explicitly skip
`PROTECTED_WORDS` — `if`, `unless`, `provided`, `after`, `once`, `later`,
`maybe`, `promise`, etc. — to keep a perturbed row's label valid. Correct
and necessary, but it means **every augmented copy repeats the source
row's exact wording for the words that actually carry the label**. With
only ~13 source dialogues for `conditional`, that's a narrow set of
literal phrasings to generalize from to a test set drawn from different
conversations entirely.

---

## 3. What's new in v7

### 3.1 Connective paraphrase (new EDA operation)

A hand-vetted, meaning-preserving paraphrase table specifically for the
vocabulary `PROTECTED_WORDS` locks down:

```python
_CONNECTIVE_SYNONYMS = {
    "if": ["provided that", "as long as", "assuming", "so long as"],
    "unless": ["except if", "other than if"],
    "later": ["down the road", "afterward", "at a later time"],
    "promise": ["commit to", "pledge to", "vow to"],
    ...
}
```

Selected as a 5th op (`eda_augment_one(..., allow_connective=True)`),
enabled only for `conditional`/`deferred` augmentation — never for `no`
rows, which weren't the problem. This is a *separate, controlled* channel
from the general synonym table: it deliberately bypasses `_is_locked()`
to touch exactly the words the other four ops must never touch.

Verified locally against the real corpus: 68/81 `conditional`+`deferred`
rows have at least one word this op can act on, and it never alters a
`[Persuader]`/`[Persuadee]` marker count (0/81 mismatches) — it only ever
matches dictionary keys that are ordinary words, never a marker token.

### 3.2 Back-translation (README idea #4, technique A)

English → French → English round-trip via `Helsinki-NLP/opus-mt-en-fr` /
`opus-mt-fr-en`, run **per turn** — never on the raw dialogue with
markers embedded in the string sent to the translator, so there's no way
for a marker to be mistranslated or dropped:

```
dialogue → split into (speaker, turn_text) pairs by marker position
         → translate each turn_text only (fr pivot)
         → translate back to English
         → reassemble: "[Persuader]"/"[Persuadee]" + translated text
```

Sampling-based decoding (`do_sample=True, top_k=50, temperature=0.8`),
seeded deterministically per `(source_text, copy_index)` via the same
`hashlib`-based stable seeding v5 introduced for EDA — so multiple
back-translated copies of the same row are reproducible but distinct.

This produces genuinely different sentence structure, not just
word-level substitution — a diversity source EDA cannot produce on its
own, and one none of v3-v6 had tried.

### 3.3 Same total row counts as v5

| Class | v5 (pure EDA) | v7 |
|---|---|---|
| `conditional` | 6 extra copies/row | 3 back-translated + 3 EDA |
| `deferred` | 2 extra copies/row | 1 back-translated + 1 EDA |
| `no` | 1 extra copy/row (unchanged) | 1 extra copy/row (unchanged) |

Deliberately unchanged from v5's totals — isolates the comparison to
augmentation *quality* (what gets generated), not quantity (how much).

### 3.4 Defensive fallback

This is the user's last planned Kaggle run for this line of work, so the
back-translation path degrades gracefully instead of risking the run:

- Model loading (`_load_backtranslation_models`) is wrapped in a
  try/except — any failure (no internet this run, a Hub hiccup, an OOM)
  prints a warning and disables back-translation for the rest of the run.
- Each individual translation call is *also* wrapped per-row — one bad
  dialogue falls back to EDA (with the connective op) instead of aborting
  the whole augmentation pass.
- `CONFIG["use_backtranslation"] = False` skips back-translation
  entirely from the start, for a lower-risk, fully-local run if preferred.
- Cell 3c's QA check extends to sample-verify back-translated output
  (if it ran) the same way it verifies the EDA path.

### 3.5 RNG re-seeding (correctness fix)

Back-translation's sampling calls `torch.manual_seed()` internally to
make each paraphrase reproducible — but that perturbs the *global* torch
RNG state, which DataLoader shuffling, dropout, and the new heads' weight
init all depend on downstream. v7 re-seeds `random`/`numpy`/`torch`
immediately after augmentation finishes, so the rest of the run stays
exactly as reproducible as v3-v5, which never touched global RNG state
after the initial seeding.

---

## 4. Unchanged from v5

Model architecture (attention pooling + cascaded modifier head),
class-balanced focal loss, supervised contrastive auxiliary loss,
binary-macro-F1 checkpoint selection, val-tuned threshold search, the
70/15/15 split, the 3-encoder benchmark, `aug_persuadee_bias_weight=0.75`
(left as-is — the v4→v5 comparison bundles multiple changes together and
can't isolate this one parameter's effect; retuning it without more runs
would be guessing), and all reporting/plots.

---

## 5. Honest expectation-setting

`conditional` has a test-set support of **3**. Even a genuine
improvement in what the model learned can show up as a small, discrete
jump (0/3 correct → 1/3 already reads as a large F1 change) — treat any
movement here as a weak signal, not a verdict. `deferred` (support=19,
much less noisy) is the more trustworthy read on whether this
augmentation upgrade actually helped. And no augmentation strategy
manufactures new labeled information: `conditional` still has only 13
real source dialogues total. If this run still doesn't move it, the
durable fix documented since v3 — more labeled `conditional` examples —
remains the real answer.
