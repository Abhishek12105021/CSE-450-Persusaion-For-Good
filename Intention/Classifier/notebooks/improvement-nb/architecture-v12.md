# MAPL Capstone — Donation-Intent Classifier, Architecture v12-Curator

This documents `capstone-v12-curator.ipynb`, in `improvement-nb/`. It is
not a new architecture or augmentation idea — it's a specialist-routing
notebook built directly on the comparative results from four real,
completed runs (`success-run-v6.ipynb`, `ran-v9-success.ipynb`,
`ran-v10.ipynb`, `ran-v11.ipynb`), all evaluated on the identical
stratified test split.

---

## 1. What the four runs actually showed

**Binary macro-F1 (test, tuned threshold):**

| | v6 (plain) | v9 (equal-vote ens.) | v10-Coda (gated) | v11-Rosetta (multi-pivot BT) |
|---|---|---|---|---|
| RoBERTa | 0.793 | — | **0.834** ← best individual anywhere | 0.783 |
| DeBERTa-v3 | 0.797 | — | 0.800 | 0.829 |
| TOD-BERT | 0.807 | — | 0.776 | 0.793 |
| ensemble | — | 0.818 | — | — |

**Modifier F1|yes (test, tuned threshold):**

| | v6 (plain) | v9 (equal-vote ens.) | v10-Coda (gated) | v11-Rosetta (multi-pivot BT) |
|---|---|---|---|---|
| RoBERTa | 0.373 | — | 0.367 | 0.363 |
| **DeBERTa-v3** | **0.452 ← best anywhere** | — | 0.395 | 0.345 |
| TOD-BERT | 0.314 | — | 0.309 | 0.314 |
| ensemble | — | 0.381 | — | — |

Two findings, each corroborated on **val**, not just test (see the
per-encoder epoch logs in each notebook's own run):

1. v10-Coda's gated RoBERTa is the best binary result in the project
   (test 0.834; its own saved-checkpoint val macro-F1 is 0.8405, also
   the highest of any RoBERTa checkpoint across v6/v10/v11 — v6: 0.8002,
   v11: 0.8349).
2. v6's plain DeBERTa-v3 is the best modifier result in the project
   (test 0.452; its own saved-checkpoint val modifier-F1|yes is 0.6433,
   also the highest of any DeBERTa-v3 checkpoint across v6/v10/v11 —
   v10: 0.5298, v11: 0.5673). Every later change to DeBERTa-v3 —
   ensembling, gating, back-translation single- or multi-pivot — made
   its modifier head worse, never better.

Since binary and modifier are scored independently throughout this whole
project (`modifier_macro_f1_given_binary_yes` is computed against the
*true* binary label, not the model's own predicted one — see
`evaluate()`), nothing stops routing them to two different models
instead of asking one architecture to be good at both.

---

## 2. What v12-Curator does

Loads exactly two checkpoints, from two different model classes defined
side by side in the notebook:

- `HierarchicalDialogueClassifier` (v6's plain architecture) — RoBERTa's
  slot is unused, only `deberta-v3-base`'s checkpoint is loaded — used
  **only** for the modifier decision.
- `HierarchicalDialogueClassifierGated` (v10-Coda's architecture: recency
  prior + last-Persuadee-turn gating, copied verbatim) — only
  `roberta-base`'s checkpoint is loaded — used **only** for the binary
  decision.

`CONFIG["encoders"]` has 2 entries (not 3), each tagged `model_type`
(`"plain"`/`"gated"`) and `task` (`"binary"`/`"modifier"`).

### 2.1 Checkpoint disambiguation without folder-naming conventions

A plain filename search for `*roberta-base*best*.pt` would find two
files if both v10-Coda's and v6's checkpoint directories are attached as
Kaggle inputs (same encoder name, different architecture, same
filename). Rather than requiring specific Kaggle dataset folder names,
`train_one_encoder()` collects *every* matching candidate and tries each
with `model.load_state_dict(state, strict=True)` against the target
class. `HierarchicalDialogueClassifierGated` has `gate_linear.*` /
`recency_strength` parameters a plain checkpoint's state dict doesn't
contain (and a plain class rejects a state dict carrying those extra
keys) — `strict=True` itself is the disambiguator. A mismatched
candidate raises `RuntimeError` and is skipped; the correct one loads
and training is skipped entirely for that encoder.

### 2.2 Fallback: bounded fresh training

If no compatible checkpoint is found for an encoder, it trains fresh —
DeBERTa-v3 with the same OOM-safe settings carried over unchanged
(`batch_size=2`, `eval_batch_size=4`, gradient checkpointing,
`PYTORCH_CUDA_ALLOC_CONF`), RoBERTa with its normal settings. Worst
case: one DeBERTa-v3 run + one RoBERTa run — strictly less total compute
than any of v6/v9/v10/v11, which each trained three encoders.

### 2.3 The curated row

```python
curated_row = {
    "model": f"CURATED ({binary_specialist_name} binary + {modifier_specialist_name} modifier)",
    "binary_accuracy": results[binary_specialist_name]["test_binary_accuracy"],
    ...
    "modifier_macro_f1_given_binary_yes": results[modifier_specialist_name]["test_modifier_macro_f1_given_yes"],
}
```

Binary metrics come entirely from the binary specialist's own
predictions; modifier metrics come entirely from the modifier
specialist's own predictions. No cascading between the two models is
needed — the metric convention already scores them independently.

---

## 3. Avoiding past mistakes

| Past mistake | Why it doesn't recur here |
|---|---|
| DeBERTa-v3 OOM | Same fix carried over unchanged. Only one DeBERTa-v3 and one RoBERTa are ever loaded, never all three encoders × two architectures at once. |
| 5+ hour runtime (v8) | Checkpoint-reuse makes a rerun near-free if checkpoints are attached. Worst case (both missing) is one DeBERTa-v3 + one RoBERTa training run. |

---

## 4. The honest caveat

The two numbers motivating this routing (0.834 RoBERTa binary, 0.452
DeBERTa modifier) were originally identified by comparing **test-set**
results across v6/v9/v10/v11 — that's model selection informed by the
test set, a real limitation for any claim that this is provably the best
achievable configuration. It does *not* undermine the narrower claim
this notebook makes: "these two specific, already-trained checkpoints,
run together, produce these specific numbers." The val-set corroboration
in §1 (both checkpoints were also the best on val among their own
architecture's own runs, not just on test) makes the selection less
likely to be pure test-set noise, but a fully independent re-split is
the only way to close this gap completely, and that's out of scope here.
This is stated in the notebook's own final summary cell too, not just
here.

`conditional` (support=3, 13 real source dialogues total) is unmoved by
this or any prior notebook across v3–v11. Routing to a better specialist
doesn't manufacture labeled data that was never collected.
