# MAPL Capstone — Donation-Intent Classifier, Architecture v3

This documents the pipeline as it stands after three iterations: the original
v2 baseline, the speaker-aware-encoding run, and this notebook's additions
(data augmentation + label smoothing). It reflects `capstone-v3-augmented.ipynb`.

---

## 1. Task

Two-headed classification over persuader–persuadee dialogues:

- **binary_label** (`no` / `yes`) — does the dialogue end in donation intent?
- **modifier** (`none` / `deferred` / `conditional`) — if `yes`, what kind of
  commitment? Evaluated both unconditionally and conditioned on
  `binary_label == "yes"` (the framing the task spec actually cares about).

---

## 2. Data pipeline

```
Raw CSV (1017 rows)
   │
   ├─ column mapping / cleanup / dedup
   ├─ stratified 70/15/15 split (stratified on binary×modifier joint stratum)
   │
   ▼
train_df (711) ── val_df (153) ── test_df (153)
   │
   ▼
EDA AUGMENTATION (train_df only, post-split)   ← new in v3
   │  - protected-keyword-guarded synonym replacement / swap / deletion / insertion
   │  - +6 copies per (yes, conditional) row      [~9-13 real → ~65-90 total]
   │  - +2 copies per (yes, deferred) row          [~48 real → ~144 total]
   │  - +1 copy per (no) row
   │  - `none` rows: untouched (already majority)
   ▼
augmented train_df  →  fed to all three encoders
```

Val/test are never touched by augmentation — evaluation numbers stay
comparable across all three notebook versions.

---

## 3. Model architecture (per encoder)

```
Dialogue text
   │
   ├─ Tokenizer (AutoTokenizer, max_len=256, return_offsets_mapping=True)
   │
   ▼
Shared Transformer Encoder  (RoBERTa-base | DeBERTa-v3-base | TOD-BERT)
   │
   ▼
last_hidden_state  [B, L, H]
   │
   ├──(+)── Speaker-Role Embedding  nn.Embedding(3, H)
   │         role_ids ∈ {Persuader=0, Persuadee=1, special/pad=2}
   │         computed from [Persuader]/[Persuadee] markers via character
   │         offsets — NOT a hardcoded token list, works across all three
   │         tokenizers (BPE + SentencePiece) uniformly.
   │         Added elementwise to hidden states BEFORE pooling.
   ▼
Masked mean-pool over non-pad tokens
   │
   ▼
Dropout(0.1)
   │
   ├──────────────┬──────────────────┐
   ▼               ▼
binary_head      modifier_head
(Linear, 2-cls)  (Linear, 3-cls)
```

---

## 4. Loss

```
binary_loss   = CE(binary_logits, binary_labels;
                    weight=inverse_freq(train, ALL rows),
                    label_smoothing=0.1)                        ← v3: smoothing added

modifier_loss = CE(modifier_logits[yes_mask], modifier_labels[yes_mask];
                    weight=inverse_freq(train, YES-ONLY rows),
                    label_smoothing=0.1)                        ← v3: smoothing added
                (0 if no "yes" rows in batch)

total_loss = 1.0 * binary_loss + 0.7 * modifier_loss
```

Key design choices baked in from earlier iterations:
- **Single imbalance strategy** (class weights only). `WeightedRandomSampler`
  oversampling is disabled — stacking it with class weights was found to
  over-rotate the model toward minority classes and collapse modifier
  macro-F1 *below* the majority baseline.
- **Modifier loss/weights masked to `binary_label=="yes"` rows.** Computing
  them over all rows (where `no` rows are hard-coded `modifier="none"`)
  diluted the true yes-conditioned class distribution and mismatched the
  evaluation metric.
- **Label smoothing (v3)** on both heads — targets the majority-class
  overconfidence collapse observed in DeBERTa's modifier head (it had
  driven to predicting `none` for 100% of test rows).

---

## 5. Training loop

- AdamW, `eps=1e-6` (raised from the PyTorch default `1e-8` — the smaller
  default was implicated in DeBERTa-v3's NaN-loss instability).
- Linear warmup + decay schedule.
- Gradient clipping (`max_grad_norm=1.0`).
- NaN-loss batches are skipped defensively, but with the `eps` fix and
  DeBERTa-specific LR (`5e-6`, `warmup_ratio=0.10`), this no longer fires
  in practice.
- Early stopping: patience=5 epochs on `(binary_f1 + modifier_macro_f1_given_yes)/2`,
  best checkpoint reloaded before final evaluation. `num_epochs` raised to
  25 (from 6) — safe because the best-checkpoint mechanism means extra
  epochs can only help or be a no-op, not overfit the reported result.

---

## 6. Evaluation

- Standard argmax metrics **and** a validation-set-tuned binary decision
  threshold (grid search over `P(yes) ≥ t` for `t ∈ [0.10, 0.90]`,
  maximizing binary macro-F1). Both are reported side by side — the tuned
  threshold is not blindly trusted, since on a ~150-row val set it can
  overfit (observed with DeBERTa: tuned threshold performed *worse* on
  test than the untuned 0.5 default).
- Modifier metrics reported both unconditionally and conditioned on
  `binary_label == "yes"` (the latter matches the task spec's framing).
- Majority-class baseline computed on the same test split for fair
  comparison, not the whole dataset.

---

## 7. Known remaining limitation

`conditional` has ~9–13 real training examples pre-augmentation. Even with
6x EDA augmentation, all synthetic copies derive from a handful of source
dialogues, so the class's *effective* diversity is still low — augmentation
buys the model more gradient signal per epoch, not new information. Treat
any `conditional` F1 improvement in this run as a partial mitigation, not
a solved problem; the durable fix is collecting more labeled `conditional`
examples.
