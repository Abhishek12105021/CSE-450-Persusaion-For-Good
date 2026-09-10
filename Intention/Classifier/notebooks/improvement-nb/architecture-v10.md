# MAPL Capstone — Donation-Intent Classifier, Architecture v10-Coda

This documents `capstone-v10-coda.ipynb`, in `improvement-nb/`. It forks
`../capstone-v6-hierarchical.ipynb` and implements README idea #9:
**Last-Persuadee-Turn Gating & Recency Prior**. Only the model class
changes — loss, augmentation, and training loop are v6's, unchanged.
Diffing the two notebooks confirms only 6 of 41 cells differ (intro,
config, the two model cells, one header, the summary).

---

## 1. Why isolate this from v8/v9

v8 stacked back-translation onto v6; v9-Oracle stacked ensembling onto
v6. Each already tests one change. Stacking a third (this gating
mechanism) onto either would make it impossible to tell which change
produced any difference in the numbers. v10-Coda adds *only* the
gating/recency mechanism to the exact v6 base — its effect is directly
readable against `../ran-nb/success-run-v6.ipynb`'s results, nothing else
in the pipeline moved.

---

## 2. What README idea #9 says, and what's implemented

> *In persuasion dialogues, opening turns are pleasantries. Donation
> commitments and condition clauses are overwhelmingly concentrated in
> the final 1–3 persuadee turns... adding an explicit architectural prior
> guarantees that the concluding stance directly influences the
> classification heads.*

Two complementary mechanisms added to `HierarchicalDialogueClassifier`:

### 2.1 Recency prior

One learned scalar (`self.recency_strength`, `nn.Parameter`, init `0.0`)
biases the existing turn-attention-pooling scores toward later turns —
a linear ramp over turn position, `0` at the first turn and
`recency_strength` at the last, added to the scores *before* the softmax
in `_attention_pool`:

```python
positions = torch.arange(U, device=hidden.device, dtype=scores.dtype)
recency_bias = self.recency_strength * (positions / max(U - 1, 1))
scores = scores + recency_bias.unsqueeze(0)
```

Starts as a complete no-op (multiplying by `0.0`) — training decides
whether pushing it positive (favoring later turns generally) helps.

### 2.2 Last-Persuadee-Turn gating

After the dialogue transformer, `_last_persuadee_index()` finds, per
batch item, the index of the dialogue's **last real turn spoken by the
Persuadee** — using `role_ids` and `utt_mask`, tensors already computed
for the existing role/position embeddings, no new inputs needed:

```python
is_persuadee_valid = (role_ids == ROLE_PERSUADEE_ID) & (utt_mask == 1)
persuadee_idx = torch.where(is_persuadee_valid, idx_range, -1).max(dim=1).values
# falls back to the last real turn of ANY role if no Persuadee turn exists
```

`dialogue_hidden` is read out at that index (`u_last` — the context-
enriched hidden vector, already having attended over the whole dialogue
via the dialogue transformer, not a raw pre-transformer turn vector) and
blended with the attention-pooled summary via a learned sigmoid gate:

```python
gate = torch.sigmoid(self.gate_linear(torch.cat([pooled, u_last], dim=-1)))
shared = gate * pooled + (1.0 - gate) * u_last
```

This is a *hard* guarantee the closing stance reaches the classifier
directly, complementing the *soft* recency prior above (which only
reweights what attention pooling already sees, rather than reading out a
specific turn independently of what pooling decided to attend to).

### 2.3 Safe initialization

`gate_linear`'s weight is zero-initialized and its bias set to `+3.0`
(`sigmoid(3.0) ≈ 0.95`), so at the start of training `shared ≈ pooled` —
matching v6's exact behavior. Combined with the recency prior's `0.0`
init, **the model starts training identical to v6** and only deviates if
gradient descent finds a reason to. This mirrors the same "start near the
known-good baseline" principle already used for the role/position
embeddings' small-std init in v6.

---

## 3. Avoiding past mistakes

| Past mistake | Why it doesn't recur here |
|---|---|
| DeBERTa-v3 OOM | Every v6 fix carried over unchanged (`batch_size=2`/`eval_batch_size=4` for DeBERTa-v3, gradient checkpointing on all three encoders, `PYTORCH_CUDA_ALLOC_CONF`). The new mechanism adds one `Linear(2H,H)` and one scalar parameter — negligible memory, no new transformer layers. |
| 5+ hour runtime (v8) | Augmentation is v6's plain EDA, not back-translation. Training cost should track v6's ~2-3 hr. |

---

## 4. What to check in the results

- Does `modifier_macro_f1|yes` — especially `deferred` (support=19), the
  class idea #9's own motivation targets ("promised later" vs. "none,
  immediate") — improve over v6's numbers?
- Print `model.recency_strength.item()` after training, per encoder: if
  it stayed near `0`, the model didn't find the recency prior useful; if
  it moved meaningfully positive, that's a direct, checkable confirmation
  of the idea's premise, not just an F1 number that could have moved for
  other reasons.
- `conditional` (support=3, only 13 real source dialogues total): an
  architectural prior doesn't manufacture new information. If it's still
  at or near 0 F1, that continues to point at labeled-data scarcity, not
  this mechanism, as the ceiling.
