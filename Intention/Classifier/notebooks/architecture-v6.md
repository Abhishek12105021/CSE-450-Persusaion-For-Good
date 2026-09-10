# MAPL Capstone — Donation-Intent Classifier, Architecture v6

This documents `capstone-v6-hierarchical.ipynb`, a fork of v5
(`capstone-v5-augfix.ipynb` — see [architecture-v5.md](architecture-v5.md)).
Data pipeline, EDA augmentation, and loss are unchanged. **The model is
replaced** with README idea #2, the Hierarchical Dialogue Encoder.

---

## 1. Why this idea, and why now

v3 through v5 all encode each dialogue as one flat token sequence,
truncated to `max_length=256`. Checked against the real dataset
(`dataset-persuassion/Manual_Label.csv`, 1017 rows):

```
words/dialogue:  mean=366.5  median=344  p90=548  p95=619  p99=814  max=1261
```

256 tokens covers roughly 180-220 English words for these tokenizers —
**below the median dialogue length**. So the flat encoder was truncating
a *typical* dialogue, not just long outliers, and always from the same
end: whatever comes after ~200 words is simply never seen. Per
`guideline.md`'s rule of thumb #2 ("use the persuadee's last clear
position, if it changes during the conversation"), the part of the
dialogue most likely to carry the actual label is exactly the part most
at risk of falling past that cutoff on a long conversation. This is a
plausible structural cause of weak performance that's independent of
anything the loss or pooling changes in v4/v5 could fix — those all
still forward-pass on the same truncated 256-token input.

---

## 2. Architecture

```
Dialogue text
   │
   split_into_utterances(): regex-position split on [Persuader]/[Persuadee]
   │  (marker-safe the same way v5's augmentation fix is; max_utterances=32,
   │   truncates from the EARLIEST turn if ever exceeded — never fires on
   │   this corpus, max observed = 30 turns)
   ▼
u1  u2  u3  ...  uU                    (U turns, per-dialogue, dynamic per batch)
   │
   flatten [B, U, L] -> [B*U, L], ONE forward pass
   ▼
Shared Utterance Encoder  (RoBERTa-base | DeBERTa-v3-base | TOD-BERT)
   │
   masked mean-pool each turn -> [B*U, H] -> reshape [B, U, H]
   │
   ├──(+)── Speaker-Role Embedding   nn.Embedding(3, H)   {Persuader, Persuadee, pad}
   ├──(+)── Turn-Position Embedding  nn.Embedding(max_utterances, H)
   ▼
Dialogue Transformer  (nn.TransformerEncoder, 4 layers, 8 heads, batch_first)
   src_key_padding_mask = ~utt_mask
   ▼
Attention pooling over turns (same learned-score mechanism as v4/v5,
one level up: over turns instead of tokens)
   ▼
shared_repr [B, H]
   │
   ├──────────────┬──────────────────────────────────────────┐
   ▼                                                          ▼
binary_head                                            modifier_head        (cascaded, unchanged from v4/v5)
(Linear, 2-cls)                    input = [shared_repr ; softmax(binary_logits).detach()]
   │                                Linear(H+2, H/2) → GELU → Dropout → Linear(H/2, 3)
binary_logits                                          modifier_logits
```

### Design notes

- **One flattened forward pass, not a per-turn Python loop.** `[B, U, L]`
  reshapes to `[B*U, L]` for a single batched encoder call, then reshapes
  back — this is what keeps the hierarchical encoder computationally
  tractable rather than `U` times slower.
- **Speaker-role + turn-position embeddings moved to the turn level.**
  v4/v5's role embedding worked at the *token* level inside one mixed-speaker
  sequence (needed because both speakers' text shared one sequence). Here
  each turn is single-speaker by construction (the dialogue is pre-split),
  so role is added once per turn-vector. Turn-position is new: the flat
  model relied on the encoder's own positional embeddings within one
  sequence; the dialogue transformer needs its own notion of turn order
  over the *reduced* sequence of turn-vectors, since it has no built-in
  positional signal of its own.
- **Utterance splitting is marker-safe** (regex `finditer` position-based,
  not `text.split(" ")`) for the same reason v5's augmentation fix needed
  to be: many markers in this corpus are glued to `\n` with no space. This
  is why v6 forks v5 specifically — splitting augmented rows into turns
  only works reliably because v5 already guarantees augmented text keeps
  its markers intact.
- **Padding turn-slots get a safe 1-token dummy** (`CLS`/`BOS` id,
  `attention_mask=1` at position 0 only) rather than an all-zero attention
  mask, to avoid depending on masked-attention edge-case behavior being
  identical across RoBERTa/DeBERTa-v3/TOD-BERT's implementations.
  `utt_mask` excludes these slots from the dialogue transformer's
  attention and from the final pooling either way, so their vector never
  reaches the heads.
- **Cascaded modifier head** is unchanged from v4/v5.

---

## 3. Loss, augmentation, evaluation — unchanged from v4/v5

Class-balanced focal loss, supervised contrastive auxiliary loss on
`shared_repr`, cascaded modifier head, binary-macro-F1 checkpoint
selection, val-tuned binary threshold search, EDA augmentation
(marker-safe tokenizer, deterministic seeding, Persuadee-turn bias) — all
identical to v5, since `compute_losses`/`evaluate`/
`find_optimal_binary_threshold` only touch `(binary_logits,
modifier_logits, shared)` and label tensors, not model internals.

---

## 4. Config changes from v5

| Key | v5 | v6 | Why |
|---|---|---|---|
| `max_length` | 256 | *(removed)* | superseded by per-turn budget below |
| `max_utt_len` | — | 64 | per-turn token cap; covers 98.7% of turns fully |
| `max_utterances` | — | 32 | per-dialogue turn cap; real max is 30, so this never truncates |
| `dialogue_num_layers` | — | 4 | README's HiTrans sketch suggests 6; lowered given the small dataset (~1000 augmented training dialogues) — a deep transformer over ~20 turn-vectors per example risks overfitting faster than it helps here |
| `dialogue_num_heads` | — | 8 | standard for hidden=768 |
| `batch_size` (dialogues/step) | 16 | 8 | `[B,U,L]` flattens to `B×U` effective sequences per encoder forward pass; memory pressure per step is higher even though each sequence is much shorter |
| `deberta-v3-base` batch_size | 8 | 2 *(was 4, see §7)* | DeBERTa-v3 already needed the largest cut in v3-v5; needs it again here |
| `eval_batch_size` | 32 | 16 (4 for DeBERTa-v3, see §7) | same reasoning as `batch_size` |

Per-class augmentation multipliers, `aug_alpha`, the protected-word list,
`cb_beta`, `focal_gamma`, and the contrastive weights are all unchanged.

---

## 7. Post-run fix: DeBERTa-v3 OOM

The first run of this notebook OOM'd partway into DeBERTa-v3 (the 2nd of
3 encoders) — see `ran-nb/failed-ran-v6.ipynb`. **RoBERTa-base completed
its full run first**, reaching `val_binary_macroF1=0.80` and
`val_modifier_macroF1|yes=0.67` — far above anything v3-v5's flat encoder
produced (0.62-0.69 / 0.28-0.34 across all their runs) — so the crash was
a memory-sizing problem, not a design problem; the hierarchical approach
itself was working as intended.

DeBERTa-v2/v3's disentangled attention builds extra `O(L²)`
content-to-position/position-to-content bias tensors per layer that
RoBERTa/BERT-style attention doesn't need, so it needs a much larger
batch-size cut here than the flat model ever did (where `batch_size=8`
was sufficient). Fixed via three changes:

1. DeBERTa-v3's `batch_size` cut from 4 to 2, plus a new
   `eval_batch_size=4` override (the per-encoder override previously only
   applied to the training batch size — extended to eval too).
2. **Gradient checkpointing** enabled on the utterance encoder for all
   three encoders (`AutoModel.gradient_checkpointing_enable()`, guarded
   by `hasattr`) — trades ~20-30% extra compute for a large cut in
   activation memory, the actual lever that addresses a flattened
   `[B*U, L]` forward pass storing activations for many more sequences
   per step than the flat model ever did.
3. `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` set before torch
   initializes its CUDA allocator (`os.environ.setdefault(...)` at the
   top of the imports cell) — directly what the OOM error message itself
   suggested, mitigating allocator fragmentation.

This is an estimate, not a guarantee — no local GPU was available to
verify against. If DeBERTa-v3 still OOMs on a re-run, the next lever is
dropping its `batch_size` to 1 in `CONFIG["encoders"]`.

---

## 5. Compute cost

This is a heavier architecture than v3-v5, by the README's own
classification ("high effort"). Expect **~1-3+ hours for all three
encoders on a free Kaggle T4**, versus v3-v5's ~15-20 min — a real
tradeoff, not a config oversight. To get a faster first read: trim
`CONFIG["encoders"]` to one entry, or lower `num_epochs` /
`early_stopping_patience`.

---

## 6. Known remaining limitation

Unchanged from v3-v5: `conditional` has only ~9-13 real training examples.
The hierarchical encoder addresses truncation and discourse structure,
not data scarcity — it cannot manufacture information that was never
labeled. Compare `classifier_test_results_v6.csv` against v5's,
particularly on longer dialogues, to see whether the added compute cost
is earning its keep on this dataset. If `conditional` is still the weak
point, the durable fix is still more labeled `conditional` examples.
