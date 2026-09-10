# MAPL Capstone — Donation-Intent Classifier, Architecture v13-Solo

This documents `capstone-v13-solo.ipynb`, in `improvement-nb/`. It forks
`capstone-v10-coda.ipynb` — the best individual result in the project so
far — and removes the modifier head entirely, per the course
instructor's review: stop splitting model capacity and training signal
across two tasks when one of them (`modifier`) is fundamentally
data-starved, and focus everything on the binary decision.

---

## 1. Why v10-Coda is the base

Across v6/v9/v10/v11 (all evaluated on the identical stratified test
split — see `architecture-v12.md` §1), v10-Coda's gated RoBERTa produced
the best individual binary macro-F1 in the whole project: 0.834 on test,
corroborated at 0.8405 on val (the highest val score any RoBERTa
checkpoint reached across v6/v10/v11). It is also the most
architecturally distinct single-model idea tried (recency prior +
last-Persuadee-turn gating, README idea #9) — v11 by contrast is v6's
architecture with a different augmentation pipeline, not a new
architecture. Both "best score" and "best architecture" point to the
same notebook.

---

## 2. What changed

### 2.1 Removed

- `self.modifier_head` (the cascaded `Linear(H+2, H/2) -> GELU ->
  Dropout -> Linear(H/2, 3)` MLP that took `[shared ;
  softmax(binary_logits).detach()]` as input) — deleted from
  `__init__`.
- `modifier_logits` from `forward()`'s return value — now `(binary_logits,
  shared)`, a 2-tuple, not v10-Coda's 3-tuple.
- `modifier_loss_weight`, `contrastive_weight_modifier`,
  `modifier_focal_loss_fn` and its class-weight computation, all
  modifier-column tracking in `evaluate()`, the averaged
  `(binary+modifier)/2` checkpoint-selection score, the modifier
  confusion-matrix cell, and the modifier classification report.

### 2.2 Kept unchanged (the architecture actually being tested)

- The gated hierarchical encoder itself: shared per-turn utterance
  encoding, role/position embeddings, the 4-layer dialogue Transformer,
  recency-biased turn-attention pooling, and last-Persuadee-turn gating
  — byte-for-byte identical to v10-Coda.
- Augmentation (v6's plain EDA), all three encoders (RoBERTa, DeBERTa-v3,
  TOD-BERT), and every OOM-safety setting.

### 2.3 Capacity reinvested in the one head that's left

- `binary_head`: `Linear(H, 2)` → `Linear(H, H/2) -> GELU -> Dropout ->
  Linear(H/2, 2)` — the exact shape the deleted `modifier_head` used to
  have, redirected.
- `contrastive_weight_binary`: `0.10` → `0.30` (v10-Coda's
  `contrastive_weight_modifier` value, moved rather than split).
- Checkpoint selection: `val_binary_macro_f1` alone, not averaged with a
  modifier score that had only 3 `conditional` / 19 `deferred` val
  examples to estimate from.

---

## 3. The one honest caveat

Augmentation is left exactly as v10-Coda had it, including the
minority-oversampling that targeted `conditional`/`deferred`
(modifier-minority classes — all `binary_label="yes"` by definition,
since modifier is only defined when the answer is yes). This notebook no
longer scores modifier, so that oversampling now just means the training
set is skewed slightly further toward `yes` than the binary label's own
imbalance requires. Left unchanged on purpose, to isolate the head-
removal + capacity-reinvestment effect from any data-side change —
retargeting augmentation at binary-minority (`no`) oversampling is the
natural next experiment if this notebook's own `no`-class numbers turn
out to be the bottleneck.

---

## 4. Avoiding past mistakes

| Past mistake | Why it doesn't recur here |
|---|---|
| DeBERTa-v3 OOM | Every fix carried over unchanged (`batch_size=2`/`eval_batch_size=4`, gradient checkpointing, `PYTORCH_CUDA_ALLOC_CONF`). Removing a head only shrinks the model. |
| 5+ hour runtime (v8) | Same augmentation and training loop as v10-Coda (~2-3 hr territory), no back-translation. |

---

## 5. What to check in the results

- Does RoBERTa's binary macro-F1 beat 0.834? Does the *ranking* of the
  three encoders change now that DeBERTa-v3 and TOD-BERT aren't sharing
  gradient signal with a modifier loss they were never that good at
  (v10-Coda modifier F1|yes: 0.395 / 0.309)?
- `no`-class F1 specifically, given the augmentation caveat in §3.
