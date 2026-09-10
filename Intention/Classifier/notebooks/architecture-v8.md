# MAPL Capstone — Donation-Intent Classifier, Architecture v8

This documents `capstone-v8-hierarchical-augplus.ipynb`, which combines
two changes that had only been tested separately: v6's hierarchical
dialogue encoder (OOM-fixed — see [architecture-v6.md](architecture-v6.md))
and v7's augmentation upgrade (see [architecture-v7.md](architecture-v7.md)).
Diffing v8 against the fixed v6 confirms only 9 of 41 cells differ
(intro, install-deps, config, the augmentation + QA cells, one header,
the summary) — model, loss, and the entire training loop are byte-for-byte
v6's.

---

## 1. Why combine them

### v6's one completed run was a big jump

v6's first run OOM'd on DeBERTa-v3, but RoBERTa-base (the 1st of 3
encoders) completed fully before the crash:

| Metric | v3-v5 flat model (range, all runs) | v6 RoBERTa (hierarchical) |
|---|---|---|
| binary macro-F1 | 0.610 – 0.698 | **0.80** (val, best epoch) |
| modifier macro-F1\|yes | 0.277 – 0.336 | **0.67** (val, best epoch) |

Not an incremental gain — a different regime. Median dialogue length is
~344 words; the flat model's 256-token cap was truncating the typical
dialogue, and per `guideline.md` that usually costs exactly the part of
the dialogue that decides the label. The hierarchical encoder removes
that truncation almost entirely.

### v7's augmentation upgrade, tested on the flat model, didn't clearly help

| Class | v5 F1 (roberta/deberta/todbert) | v7 F1 (roberta/deberta/todbert) |
|---|---|---|
| `conditional` (support=3) | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 |
| `deferred` (support=19) | 0.09 / 0.13 / 0.00 | 0.05 / 0.06 / 0.00 |
| binary macro-F1 | 0.648 / 0.670 / 0.623 | 0.610 / 0.698 / 0.611 |

Back-translation and the connective-paraphrase op both ran correctly
(0% marker corruption verified on both paths, `ran-nb/ran-v7.ipynb` cell
14). This is evidence the flat model's bottleneck wasn't minority-class
phrasing diversity — plausibly it was truncation, which v7 never
addressed. The natural next experiment: apply v7's augmentation
diversity to the architecture that already showed truncation removal
matters, instead of concluding augmentation quality doesn't matter.

---

## 2. What v8 actually is

- **Model**: `HierarchicalDialogueClassifier`, verbatim from the
  OOM-fixed v6 (reduced DeBERTa-v3 batch size + eval batch size,
  gradient checkpointing on all three encoders, `PYTORCH_CUDA_ALLOC_CONF`).
- **Augmentation**: v7's pipeline verbatim — connective paraphrase EDA
  op + per-turn back-translation for `conditional`/`deferred`, same
  total row counts as v5 (isolating quality vs. quantity), same
  defensive EDA fallback if back-translation fails to load.
- **Loss / training loop**: class-balanced focal loss, supervised
  contrastive auxiliary loss, binary-macro-F1 checkpoint selection,
  val-tuned threshold search — v6's, unchanged.

The two pieces compose cleanly because augmentation only ever touches
`train_df["text"]` (plain strings) — it has no dependency on how the
model later consumes that text. The hierarchical model's collate
function turn-splits augmented rows exactly the same way it splits real
ones (both v6 and v7 already use the same regex-position marker-splitting
principle, just at different points in the pipeline).

---

## 3. One thing neither parent could tell us alone

Back-translated turns come out shorter and structurally different after
a round-trip through French (see the samples in `ran-nb/ran-v7.ipynb`
cell 14 — e.g. "Save the Children" round-tripping into something close to
"avoiding giving children"). v7's flat model truncates at 256 tokens
regardless, so this never interacted with truncation there. The
hierarchical model preserves per-turn structure through to the
classifier, so it's worth checking in this run's output whether
back-translated turns behave differently under `max_utterances`/
`max_utt_len` than the original EDA-perturbed text did — something the
flat-model run had no way to surface.

---

## 4. Config

Union of v6's hierarchical settings (`max_utterances=32`, `max_utt_len=64`,
`dialogue_num_layers=4`, the OOM-fixed per-encoder batch sizes) and v7's
augmentation settings (`aug_num_conditional_bt/eda`, `aug_num_deferred_bt/eda`,
`use_backtranslation`, `backtranslation_pivot_lang`). No key conflicts —
the two parents touched disjoint parts of `CONFIG`. `run_tag="v8"`,
`checkpoint_dir_name="checkpoints_v8"`, outputs suffixed `_v8`.

---

## 5. Compute cost

Same profile as the fixed v6 (1-3+ hours for all three encoders on a
free T4), plus the few extra minutes v7 already paid once for
back-translation model download and the one-time augmentation pass
before training starts.

---

## 6. What to look for in results

Two questions this run can answer that neither v6 nor v7 alone could:

1. **Does the augmentation upgrade compound with the architecture fix**,
   or does the hierarchical encoder's gain dominate regardless of
   augmentation source (v8 ≈ v6-fixed's numbers)? Either answer is
   informative — it settles whether v7's augmentation upgrade was
   solving the wrong problem on its own, or just needed truncation fixed
   first to show its effect.
2. **Does `conditional` move at all.** It has only 13 real source
   dialogues in any architecture tried so far (v3-v7, all at 0.00 F1). If
   it's still at or near 0 here, that's a strong signal the remaining
   ceiling is labeled-data scarcity, not architecture or augmentation —
   consistent with the "known limitation" flagged since v3.
