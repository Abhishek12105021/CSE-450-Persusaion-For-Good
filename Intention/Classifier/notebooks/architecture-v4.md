# MAPL Capstone — Donation-Intent Classifier, Architecture v4

This documents `capstone-v4-focal-contrastive.ipynb`, a fork of v3
(`capstone-v3-augmented.ipynb`, kept unchanged as the running baseline —
see [architecture.md](architecture.md)). Same data, same 70/15/15 split,
same 3-encoder benchmark. What changed is the model architecture, the
loss, and one training-loop bug in checkpoint selection.

**Trigger for this fork:** v3 was reported to collapse toward the
majority classes — predicting `binary_label="yes"` and `modifier="none"`
regardless of input, rather than learning the minority classes, despite
inverse-frequency class weights already being in the loss.

---

## 1. Root cause found while reading v3

`train_one_encoder()`'s checkpoint selection / early-stopping signal was:

```python
val_score = (val_metrics["binary_f1"] + val_metrics["modifier_macro_f1_yes"]) / 2
```

`val_metrics["binary_f1"]` is `f1_score(..., average="binary", pos_label=yes_idx)`
— **F1 of the `yes` class only**. A model that always predicts `yes` gets
100% recall on that one class and scores *well* on this metric, since it
never measures `no`-class recall. The metric used to decide which epoch's
checkpoint to keep could reward exactly the collapse behaviour it should
have penalised. (`find_optimal_binary_threshold()` already searched for
macro-F1 — only the per-epoch checkpoint-selection metric had the bug.)

---

## 2. What changed

| # | Change | Where | Rationale |
|---|---|---|---|
| 1 | Checkpoint selection / early stopping uses binary **macro**-F1 (avg of `no`-F1 and `yes`-F1), not yes-only F1 | training loop | Direct fix for the bug above — free, and likely the single highest-leverage change |
| 2 | **Class-Balanced Focal Loss** (Cui et al., 2019, CVPR) replaces weighted CE + label smoothing on both heads | loss | Effective-number-of-samples weighting saturates gracefully for near-zero classes (`conditional`, ~9-13 real rows) instead of an exploding inverse-frequency ratio; the `(1-p_t)^gamma` focal term keeps discounting easy/majority predictions for the whole run instead of a fixed static weight the model can learn around |
| 3 | **Attention pooling** (fused with `[CLS]`) replaces masked mean-pooling | model | Mean-pooling spreads weight evenly across a whole dialogue, diluting the few tokens that actually carry modifier signal (`"if"`, `"next month"`, hedges, negation); a learned per-token score lets the model find them |
| 4 | **Cascaded modifier head**: takes `[shared_repr ; softmax(binary_logits).detach()]` as input | model | Makes the task's real binary→modifier dependency explicit to the modifier head itself, not just implicit through the yes-only masked loss |
| 5 | **Supervised Contrastive auxiliary loss** (Khosla et al., 2020), in-batch, single-stage | loss | Lightweight stand-in for README idea #3 — full SimCSE needs a separate unsupervised-pretraining stage, which doesn't fit the ~20-30 min budget. This version reuses the batch's already-computed pooled vectors (one `B×B` similarity matrix, ~free compute) to directly pull same-class representations together, including the classes that were collapsing |

Kept unchanged from v3 (not implicated in the collapse): speaker-role
embeddings (README idea #1), EDA augmentation (README idea #4), the
70/15/15 stratified split, val-tuned binary threshold search, the
3-encoder sweep, and all plotting/reporting cells.

**Deliberately not done** (would blow the "keep it fast, ~20-30 min"
budget): the hierarchical utterance encoder (README idea #2 — doubles
encoder passes) and a full two-stage SimCSE contrastive-pretraining phase
(README idea #3-full, needs a separate training run before fine-tuning).

---

## 3. Model architecture (per encoder)

```
Dialogue text
   │
   Tokenizer (AutoTokenizer, max_len=256, return_offsets_mapping=True)
   │
Shared Transformer Encoder  (RoBERTa-base | DeBERTa-v3-base | TOD-BERT)
   │
last_hidden_state  [B, L, H]
   │
   ├──(+)── Speaker-Role Embedding  nn.Embedding(3, H)          [unchanged from v3]
   │
   ├───────────────────┬────────────────────────┐
   │                    │                        │
[CLS]/<s> vector   Attention pooling              │  ← NEW (replaces mean-pool)
   [B, H]          score_t = v^T tanh(W h_t)      │
   │               weights = softmax_t(score_t | non-pad)
   │               pooled  = Σ_t weights_t · h_t   [B, H]
   └───────────────────┴────────────────────────┘
              concat → Linear(2H, H) → GELU → Dropout
                              │
                        shared_repr [B, H]
                              │
              ┌───────────────┴───────────────┐
              ▼                                ▼
        binary_head                     modifier_head          ← NEW: cascaded
      (Linear, 2-cls)     input = [shared_repr ; softmax(binary_logits).detach()]
              │             Linear(H+2, H/2) → GELU → Dropout → Linear(H/2, 3)
       binary_logits                    modifier_logits
```

---

## 4. Loss

```
binary_focal   = ClassBalancedFocalLoss(binary_logits, binary_labels)
                 weights from effective-number-of-samples(train, ALL rows, beta=0.999)
                 focal gamma=2.0

modifier_focal = ClassBalancedFocalLoss(modifier_logits[yes_mask], modifier_labels[yes_mask])
                 weights from effective-number-of-samples(train, YES-ONLY rows, beta=0.999)
                 (0 if no "yes" rows in batch)

con_binary     = SupCon(shared_repr, binary_labels)                    weight 0.10
con_modifier   = SupCon(shared_repr[yes_mask], modifier_labels[yes_mask])  weight 0.30
                 (0 if fewer than 2 yes-rows in batch)

total_loss = 1.0 * binary_focal + 0.7 * modifier_focal
             + 0.10 * con_binary + 0.30 * con_modifier   (training only;
             eval-time loss reporting omits the contrastive terms — they
             shape representations, they aren't a prediction-quality metric)
```

SupCon is computed per-batch on already-produced pooled vectors (one
`B×B` cosine-similarity matrix), so it adds no extra encoder forward
passes — the reason this fits inside the same compute budget as v3.

---

## 5. Training loop

Unchanged from v3: AdamW (`eps=1e-6`), linear warmup+decay, gradient
clipping (`max_grad_norm=1.0`), NaN-loss batches skipped defensively,
DeBERTa-specific LR (`5e-6`, `warmup_ratio=0.10`, `batch_size=8`),
`num_epochs=25` with best-checkpoint reload, early stopping
(`patience=5`).

**Changed:** the quantity early stopping and checkpoint selection
optimize is now `(binary_macro_f1 + modifier_macro_f1_given_yes) / 2`
instead of `(binary_f1[yes-only] + modifier_macro_f1_given_yes) / 2`.

---

## 6. Evaluation

Same as v3 — argmax metrics **and** a validation-tuned binary threshold
(grid search `P(yes) ≥ t` for `t ∈ [0.10, 0.90]` maximizing macro-F1,
both reported side by side), modifier metrics reported unconditionally
and conditioned on `binary_label == "yes"`, majority baseline on the same
test split. **Added:** `binary_macro_f1` is now reported explicitly
alongside the yes-only `binary_f1` in every table, so the two are never
conflated again.

Output files are suffixed `_v4` (`classifier_test_results_v4.csv`,
`classifier_comparison_bar_v4.png`, etc.) and checkpoints go to
`checkpoints_v4/`, so this notebook can run in the same Kaggle working
directory as v3 without overwriting its artifacts.

---

## 7. Known remaining limitation

Same as v3: `conditional` has ~9–13 real training examples pre-augmentation.
Class-balanced weighting, focal loss, and the contrastive term all give the
model *better use of* that signal — none of them manufacture new
information. Treat any `conditional` F1 improvement here as a mitigation,
not a solved problem. If it's still weak after this run, the next steps
in order of effort are: ensembling the 3 already-trained encoders'
probabilities (README idea #6 — cheap, reuses these checkpoints, no
retraining), then the hierarchical utterance encoder (README idea #2 —
addresses 256-token truncation losing later dialogue turns, needs more
compute budget than used here).

---

## 8. References (new for v4)

| Citation |
|---------|
| Cui et al. (2019). *Class-Balanced Loss Based on Effective Number of Samples.* CVPR. |
| Lin et al. (2017). *Focal Loss for Dense Object Detection.* ICCV. |
| Khosla et al. (2020). *Supervised Contrastive Learning.* NeurIPS. |

(TOD-BERT, DeBERTa-v3, and EDA references carry over from
[architecture.md](architecture.md) / [README.md](README.md) — unchanged.)
