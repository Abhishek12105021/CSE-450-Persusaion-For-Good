# MAPL Capstone — Donation-Intent Classifier, Architecture v9-Oracle

This documents `capstone-v9-oracle.ipynb`, in `improvement-nb/`. It
forks `../capstone-v6-hierarchical.ipynb` — **not** v8 — and adds README
idea #6 (Ensemble + Uncertainty Estimation), the one idea from the
original list that hadn't been tried yet and doesn't require retuning
anything already validated by a real run.

---

## 1. Why fork v6 and not v8

Both `../ran-nb/success-run-v6.ipynb` and `../ran-nb/run-v8.ipynb`
finished successfully after the v6 OOM fix. Pulled from their actual
test-set results (tuned threshold, all 3 encoders — roberta / deberta-v3
/ todbert):

| Metric | v6 (plain EDA) | v8 (+ back-translation) |
|---|---|---|
| binary macro-F1 | 0.793 / 0.797 / 0.807 | 0.794 / **0.821** / 0.773 |
| modifier F1\|yes | 0.373 / **0.452** / 0.314 | 0.348 / 0.355 / 0.364 |
| `conditional` F1 (support=3) | 0.00 / **0.07** / 0.00 | 0.00 / 0.00 / 0.00 |
| wall-clock (T4, all 3 encoders) | ~2-3 hr | **5+ hr** |

v8's back-translation addition is a wash at best: it helped DeBERTa's
binary macro-F1 a little, but **cost the one non-zero `conditional`
result seen anywhere across v3-v8** (v6's DeBERTa got 1 of 3 test
`conditional` rows right; v8's got 0 of 3), knocked modifier F1\|yes down
across the board, and took roughly twice as long. Consistent with
`../architecture-v7.md`'s finding that back-translation didn't clearly
help the flat model either — apparently it doesn't reliably help the
hierarchical model either. v6 is the better, cheaper base.

---

## 2. What v9 adds

Model, loss, training loop, and augmentation are v6's, byte-for-byte —
confirmed by diffing the two notebooks (only cells 0, 4, 21-24, 28 of 41
differ before the new sections are inserted). New:

### 2.1 Checkpoint-reuse fast path

`train_one_encoder()` accepts an optional `external_ckpt_path`. Before
training each encoder, the run loop searches `CONFIG["search_roots"]`
(the same fuzzy, recursive convention already used to find the labeled
CSV) for a file matching `<encoder_name>...best...pt`. If found — e.g.
`checkpoints_v6/roberta-base_best.pt` attached as a Kaggle input dataset
from a prior run's output — it's loaded directly and the entire epoch
loop is skipped. Falls back to training fresh (identical to v6) if
nothing is found. This is the main lever against repeating v8's 5+ hour
cost: with v6's checkpoints attached, v9 becomes a matter of minutes
(inference-only), not hours.

### 2.2 MC-Dropout (README idea #6, part 1)

`run_mc_dropout_for_encoder()` reloads one encoder at a time from its
checkpoint (never holding more than one transformer in GPU memory
simultaneously — same discipline as `train_one_encoder`'s own
load/delete pattern) and runs `CONFIG["mc_dropout_samples"]` (20)
stochastic forward passes over the test set with dropout active
throughout the *whole* model — encoder, dialogue transformer, and heads,
not just the final classifier dropout — via `model.train()` under
`torch.no_grad()` (forward-only, so this is cheap regardless of gradient
checkpointing, which only affects backward-pass memory).

Produces, per row: a Monte-Carlo-averaged probability and its variance
across the 20 samples, for both heads.

### 2.3 Soft-voting ensemble (README idea #6, part 2)

The 3 encoders' MC-Dropout-mean probabilities are averaged (binary and
modifier separately). The binary decision threshold is tuned on the
ensembled **val** probabilities (each encoder's own `val_metrics`,
already captured as a side effect of `train_one_encoder`'s normal
threshold-search step) via the same grid-search logic every individual
encoder already uses — refactored into `find_optimal_threshold_from_probs()`
so it can run on a pre-computed array instead of needing a live model.
Never tuned on test, consistent with every prior notebook's methodology.

### 2.4 Uncertainty-flagged review report

Per-row uncertainty score = average within-encoder MC-Dropout variance
(each encoder's own epistemic uncertainty) **+** cross-encoder
disagreement (variance of the 3 encoders' own MC-Dropout-mean
predictions — how much the different architectures disagree). Both
signals come from README idea #6's own sketch (MC-Dropout variance,
ensemble disagreement); this combines them into one score, surfaces the
`CONFIG["uncertainty_flag_top_n"]` (10) highest-uncertainty test rows
with whether the ensemble got each one right, and reports mean
uncertainty split by correct vs. incorrect — a direct, checkable
diagnostic of whether the signal is trustworthy on this dataset, printed
inline rather than assumed.

---

## 3. Avoiding the two mistakes already made

| Past mistake | How v9 avoids repeating it |
|---|---|
| DeBERTa-v3 OOM (first v6 run) | Every fix carried over unchanged: `batch_size=2` / `eval_batch_size=4` for DeBERTa-v3, gradient checkpointing on all three encoders, `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`. Nothing about ensembling or MC-Dropout increases per-step *training* memory — MC-Dropout is inference-only under `torch.no_grad()`, and reloads one encoder at a time. |
| 5+ hour run for an unclear gain (v8) | Back-translation is not reintroduced — training-side cost tracks v6's ~2-3 hr, not v8's 5+. The checkpoint-reuse path additionally makes a *rerun* close to free if v6/v9 checkpoints are attached as an input dataset. |

---

## 4. Honest expectation-setting

Soft-voting is not guaranteed to help the rarest class. If 2 of 3
encoders essentially never assign real probability mass to
`conditional` — true in every run so far, v3 through v8 — averaging can
*dilute* the one encoder that occasionally gets it right rather than
reinforce it. The notebook checks this directly instead of assuming
ensembling is a free win: see section 12's `conditional` numbers.
`deferred` (support=19, much less noisy than `conditional`'s support=3)
remains the more informative class to watch for whether the ensemble
actually helped.

`conditional` has only 13 real source dialogues total, in any
architecture or combination strategy tried across v3-v9. If it's still
at or near 0 F1 after ensembling, that continues to point at
labeled-data scarcity as the remaining ceiling — no amount of
architecture change, augmentation, or ensembling manufactures
information that was never labeled.

---

## 5. What the actual run showed, and the fix that followed

`../ran-nb/ran-v9-success.ipynb` confirmed the checkpoint-reuse path
works exactly as designed (all 3 encoders loaded from an attached
`checkpoints_v6` dataset, training skipped entirely) and surfaced a real,
specific instance of the dilution risk flagged in §4 above:

| | binary macro-F1 | modifier F1\|yes |
|---|---|---|
| RoBERTa | 0.793 | 0.373 |
| **DeBERTa-v3** | 0.797 | **0.452** ← best individual |
| TOD-BERT | 0.807 | 0.314 |
| **Equal-vote ensemble** | **0.818** ← beats every individual | 0.381 ← *worse* than DeBERTa-v3 alone |

Binary ensembling was a clean, real win. Modifier ensembling was not —
equal-vote averaging pulled DeBERTa-v3's genuinely better modifier
predictions down toward RoBERTa's and TOD-BERT's weaker ones instead of
reinforcing them. (`conditional` recall did jump to 2/3, the best seen
across v3-v9 — but precision cratered to 0.05, i.e. the ensemble started
over-predicting `conditional` broadly rather than more accurately.)

**Fix, added in section 12a** (`### 12a. Weighted ensemble`): reweight
only the *modifier* vote by each encoder's own val-set
`modifier_macro_f1_yes` (already computed as a side effect of each
encoder's normal threshold-search step — no retraining, no new val-set
access, no test-set peeking). Binary stays equal-vote, unchanged, since
there's no evidence that needs fixing and equal-vote is what produced
the binary win. The cell reports its own before/after comparison against
both the equal-vote ensemble and the single best encoder rather than
assuming the reweighting helps — check its printed output for whether it
actually closed the gap.

One honest caveat baked into that cell's own documentation: the val
split has few `binary_label=yes` rows to begin with, and fewer still
that are `deferred`/`conditional` — the weighting basis is a genuinely
small sample and could itself be noisy on a re-run with different data.
