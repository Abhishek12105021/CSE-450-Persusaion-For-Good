# MAPL Capstone — Donation-Intent Classifier, Architecture v11-Rosetta

This documents `capstone-v11-rosetta.ipynb`, in `improvement-nb/`. It
forks `../capstone-v6-hierarchical.ipynb` and **polishes, rather than
abandons, v8's back-translation idea** — multi-pivot round-trips, a
quality/diversity decoding split, and a larger per-class copy budget.
Only the augmentation cell changes; model, loss, and training loop are
v6's, unchanged. Diffing the two notebooks confirms only 9 of 41 cells
differ (intro, install-deps, config, augmentation + QA, one header, the
summary).

---

## 1. Why this exists

`run-v8.ipynb`'s actual results showed back-translation (single
pivot — French only, sampling decoding only) didn't clearly beat plain
EDA on the hierarchical model, and cost 2x the runtime (see
`../architecture-v8.md`, `../architecture-v9.md`). That was a real
finding — but a narrow one, worth polishing before concluding the idea
itself doesn't work here:

1. **One pivot language.** Every back-translated copy of a row went
   through the identical `en→fr→en` round trip, differing only by
   sampling-decoder noise from one MT model pair — a narrow diversity
   source. Genuinely different phrasing needs genuinely different
   linguistic detours.
2. **No quality/diversity split.** Every copy used sampling decoding
   (`temperature=0.8`), good for diversity but able to drift further from
   the source meaning than intended — risky when a single badly-drifted
   copy is a meaningful fraction of an already tiny class's training
   signal (v7's own sample showed "Save the Children" round-tripping into
   something close to "avoiding giving children").

---

## 2. What's polished

### 2.1 Two pivot languages

`CONFIG["backtranslation_pivot_langs"] = ["fr", "de"]`. Each pivot loads
its own MT model pair independently (`_load_backtranslation_models`
tries each language separately, so one failing to download doesn't take
the others down) and produces a structurally different rewrite, not just
resampled noise from the same language pair.

### 2.2 Quality pass + diversity pass, per pivot

`add_backtranslation_copies` cycles pivots by copy index and alternates
decoding strategy:

```python
pivot_lang = loaded_pivots[k % n_pivots]
use_beam   = (k // n_pivots) == 0   # first pass through the pivot list = beam search
```

With 2 pivots and `n_copies=4`: `(fr, beam), (de, beam), (fr, sample),
(de, sample)` — verified locally before building the notebook. The first
pass per pivot uses **beam search** (`num_beams=4`, deterministic) for a
cleaner, lower-drift paraphrase; later passes use **sampling**
(`temperature=0.8`, seeded via the same `hashlib`-based stable seed v5
introduced) for more aggressive diversity. Both still translate per-turn
with markers reattached afterward — never sent to the translator, so a
marker itself can't be mistranslated (unchanged principle from v5/v7/v8,
verified there at 0% corruption).

### 2.3 Extended dataset

| Class | v8 (single pivot) | v11-Rosetta |
|---|---|---|
| `conditional` extra copies | 3 BT + 3 EDA = 6 | **4 BT (1 beam + 1 sample × 2 pivots) + 3 EDA = 7** |
| `deferred` extra copies | 1 BT + 1 EDA = 2 | **2 BT (1 beam × 2 pivots) + 1 EDA = 3** |

Genuinely more *and* more diverse synthetic data — not just a
re-shuffled version of the same amount, which is what "extend the
dataset" asked for.

### 2.4 Defensive design, unchanged from v7/v8

Model-loading failures per pivot, per-row translation failures, and a
global `CONFIG["use_backtranslation"] = False` kill switch all still
fall back to EDA (with the connective-paraphrase op) automatically — see
`../architecture-v7.md` for the original design rationale, carried over
unchanged here.

---

## 3. Isolated from v9-Oracle and v10-Coda, on purpose

Same principle used for v10-Coda: stacking this augmentation change onto
v9's ensembling or v10's gating would make it impossible to attribute a
result to any one change. v11-Rosetta's numbers are directly comparable
against `../ran-nb/success-run-v6.ipynb`'s (plain EDA) and
`../ran-nb/run-v8.ipynb`'s (single-pivot back-translation) — isolating
exactly what polishing the idea bought.

---

## 4. Avoiding past mistakes

| Past mistake | Why it doesn't recur here |
|---|---|
| DeBERTa-v3 OOM | Every v6 fix unchanged (`batch_size=2`/`eval_batch_size=4`, gradient checkpointing, `PYTORCH_CUDA_ALLOC_CONF`). Back-translation is a one-time data-prep step before training starts — doesn't touch training-time memory. |
| 5+ hour runtime | A second pivot language adds a one-time preprocessing cost (one more MT model pair to download/run), not a training-time multiplier. Training-side cost tracks v6's ~2-3 hr regardless of augmentation choices, since batch sizes and epoch counts are unchanged. |

---

## 5. Honest expectation-setting

This is a genuine test of whether v8's back-translation idea was
under-powered (too little diversity, too much drift) or fundamentally
not the right lever for this dataset. Both answers are useful — "needed
polish and now it helps" and "even polished, doesn't move the needle"
each settle something for the next iteration. `deferred` (support=19) is
the class to watch; `conditional` (support=3, only 13 real source
dialogues total, in any augmentation strategy tried across v3-v11) will
not be solved by better augmentation alone — no synthetic diversity
manufactures information that was never labeled.
