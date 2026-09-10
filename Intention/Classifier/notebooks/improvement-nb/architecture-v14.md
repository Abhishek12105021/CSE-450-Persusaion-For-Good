# MAPL Capstone — Donation-Intent Classifier, Architecture v14-Antiphony

This documents `capstone-v14-antiphony.ipynb`, in `improvement-nb/`. It
is a genuinely new architecture — not a variant of v6's hierarchical
encoder, unlike every notebook from v6 through v13. It forks
`capstone-v13-solo.ipynb` for everything except the model class:
data loading, augmentation, loss, and the training loop are identical,
so any difference in results is attributable to the architecture alone.

---

## 1. The structural gap every prior notebook shares

v6 through v13 all encode a dialogue as **one interleaved sequence of
turns**: shared per-turn utterance encoding → additive role + position
embeddings → a single dialogue-level Transformer over the whole
sequence → attention pooling (v10-Coda adds a recency bias and a
last-turn gate on top of this same pooled summary). Speaker role enters
only as an embedding added to an otherwise role-blind attention pass.

That discards a structural fact this task is built on: a persuasion
dialogue has two **asymmetric** roles. One party argues (Persuader), the
other decides (Persuadee), and the label is defined entirely by what the
deciding party does. A single mixed-sequence architecture has to
*rediscover* who's who from a role embedding; it never gets an explicit
"the decision-maker is responding to the arguer" signal.

## 2. The architecture

Three new mechanisms replace the single dialogue Transformer +
attention-pool + gate, entirely:

1. **Speaker-disentangled discourse encoding.** After the same shared
   per-turn utterance encoder (unchanged), turn vectors are split by
   role into a Persuader stream and a Persuadee stream — each kept in
   its own chronological order, each given its **own** 2-layer
   Transformer. This models how each party's own argument or stance
   develops across their own turns, without the other role's turns
   interleaved in between. In the same family as *DialogueRNN*'s
   per-party state tracking (Majumder et al., AAAI 2019 — built for
   emotion recognition in conversation; adapted here for persuasion
   outcome).

2. **Directional cross-attention.** `nn.MultiheadAttention` with the
   Persuadee stream as query and the Persuader stream as key/value — an
   explicit, asymmetric "how does the decision-maker's stance respond to
   what was argued" mechanism. "Antiphony" (alternating call-and-
   response between two distinct voices) names this structurally.

3. **Commitment-trajectory head.** `nn.GRU` over the cross-attended
   Persuadee stream, in chronological order; its **final** hidden state
   is a "how did commitment build up, turn by turn" signal, concatenated
   with an attention-pooled "what mattered most overall" summary of the
   same stream before the binary head. A GRU's hidden state is
   inherently shaped more by recent inputs, so recency is an emergent
   property of the mechanism, not a hand-tuned scalar (contrast
   v10-Coda's `recency_strength`).

## 3. Implementation details worth knowing

- `_split_by_role()` operates on the already-pooled `[B, U, H]` turn-
  vector tensor (same tensor every prior notebook's dialogue Transformer
  consumes), re-packing it per role into `[B, max_role_len, H]` via a
  per-batch-item loop (`B` is small — 2 to 8 — so this loop costs nothing
  next to the actual Transformer forward passes). It keeps each role's
  **last** `max_role_len` turns in original order, mirroring the
  project-wide "preserve the closing turns under truncation" convention.
  `max_role_len=20` (corpus p95 = 23 total turns/dialogue, so a single
  role's share is comfortably under 20 in the overwhelming majority of
  cases).
- Masking follows the same `True = ignore` convention used everywhere
  else in the project (`src_key_padding_mask` on both stream
  Transformers, `key_padding_mask` on the cross-attention layer). The
  GRU's trajectory readout uses `pack_padded_sequence` with each row's
  true per-role turn count, so its final hidden state is read at each
  dialogue's actual last Persuadee turn, never a padding slot —
  `enforce_sorted=False` handles arbitrary batch ordering without a
  manual sort/unsort step.
- `shared` is `[B, 2H]` (pooled summary concatenated with the trajectory
  vector), not `[B, H]` — the supervised-contrastive loss and the binary
  head's first `Linear` are sized accordingly; nothing else in the
  training loop needed to change since both still just consume `shared`
  as an opaque vector.

## 4. Why this shouldn't reintroduce the OOM/runtime mistakes

The new stream Transformers, cross-attention, and GRU all operate on
already-pooled `[B, R<=20, H]` tensors — far smaller than the `[B*U, L]`
flattened tensors the shared utterance encoder itself processes (the
actual memory-dominant step, unchanged, gradient checkpointing intact).
Two 2-layer Transformers over `R<=20` turns plus one cross-attention
layer is, if anything, cheaper than v6-v13's single 4-layer Transformer
over `U<=32` turns. No back-translation, no third augmentation pass —
same augmentation and training loop as v13-Solo.

## 5. What a result either way would mean

- If this beats v13-Solo's per-encoder binary macro-F1, that's a
  genuinely different mechanism succeeding — the architectural
  contribution worth foregrounding in a writeup, not a tuned variant of
  something already proven.
- If it doesn't, that's still informative: a materially different,
  more structurally-motivated architecture failing to move binary
  performance further is harder to explain away as "just needed a
  better encoder" than a small tweak failing would be — it would point
  toward the project's real ceiling being closer to a data-scarcity
  limit (the same story `conditional`'s near-zero F1 has told since v3)
  than an architecture-expressiveness one.
