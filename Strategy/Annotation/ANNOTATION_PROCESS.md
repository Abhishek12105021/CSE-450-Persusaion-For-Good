# Annotation Process

This document explains, step by step, how multi-label persuasion-strategy
annotation was carried out on the PersuasionForGood corpus. It describes
the general methodology used across annotation runs, independent of which
specific range of turns a given run covers. It is meant to be read
alongside:

- [`prompt.md`](./prompt.md) — the exact system prompt, taxonomy, decision
  rules, and batch protocol given to the model.
- [`TAXONOMY_CHEATSHEET.md`](./TAXONOMY_CHEATSHEET.md) — the 11-category /
  41-strategy reference table.
- [`pipeline.py`](./pipeline.py) — a script that reproduces the mechanical
  steps (batching, context windowing, prompt assembly, validation, merging)
  for review/demonstration purposes.

---

## 1. Scope & unit of annotation

- **Source data:** `persuader_turns.csv` — one row per Persuader turn across
  the PersuasionForGood corpus.
- **Batching:** the corpus is split into fixed-size batches (200 turns per
  batch in this project), processed and labeled independently.
- **Unit of annotation:** a single Persuader turn, labeled using the
  Persuadee/Persuader dialogue history immediately preceding it.

A given annotation run covers some contiguous range of rows/batches from
the source CSV; the process below is the same regardless of which range is
being run.

---

## 2. Step 1 — Batch generation

Each batch file (`batch_NN_turns_X_Y.json`) contains a fixed number of
consecutive Persuader turns, sliced directly out of `persuader_turns.csv`
by row position. Each turn object carries:

| Field | Purpose |
| --- | --- |
| `turn_id` | unique id, e.g. `20180831-063536_532_live#t004` |
| `dialogue_id` | which conversation the turn belongs to |
| `turn_index` / `persuader_turn_index` | position within the dialogue |
| `text` | the exact Persuader utterance to be labeled |
| `context` | up to 5 preceding turns, alternating `[Persuader]` / `[Persuadee]` |
| `binary_label_norm` / `modifier_norm` | pre-existing dataset labels, carried through unchanged (not used for strategy labeling) |

Batches are **not** shuffled or resampled — they preserve the original row
order and dialogue grouping, so a given dialogue's turns are usually
processed within the same batch (a dialogue that straddles a batch boundary
still has its context correctly preceding each turn, since `context` is
precomputed per-row rather than regenerated per-batch).

## 3. Step 2 — Dialogue context (5-turn window)

Each turn's `context` field is pre-computed in the source CSV: the last
**5 conversational turns** immediately preceding the turn being labeled,
formatted as alternating `[Persuader] ...` / `[Persuadee] ...` lines. This
gives the annotator (human or model) enough local history to judge
pragmatic function (e.g. whether a mention of "children suffering" is a
neutral opener or a guilt appeal following a refusal) without pasting the
entire dialogue.

Two caveats worth flagging to a reviewer:

- The context window is **turns, not characters** — a long single turn
  counts as one unit of the 5, so context length varies.
- For turns very early in a dialogue (index 0–2), `context` is shorter than
  5 turns or empty; this is expected and handled by the "Greetings &
  Closings" convention in `prompt.md` (bare openers get the empty-set
  label).

## 4. Step 3 — Prompt assembly per batch

For each batch, two pieces are combined into a single labeling request:

1. **System prompt** (`prompt.md`, Section 1) — sets the annotator's role,
   states the task definition, and embeds the full closed-world taxonomy
   (11 categories / 41 strategies) plus the **four operational decision
   tests**, applied in strict order:
   1. **Removal Test** — a candidate strategy only counts if the phrase
      supporting it can be deleted without destroying a co-occurring
      strategy's phrase.
   2. **Specific beats general** — a specific tactic (e.g.
      `evidence_and_statistics`) is preferred over tagging its broader
      parent concept (e.g. `logical_appeal`) for the same clause.
   3. **Function over keyword matching** — labels reflect what the turn
      *does* pragmatically in context, not surface trigger words.
   4. **Realistic density cap** — most turns get 1–3 labels; empty,
      non-strategic turns (bare greetings/closings) get the explicit
      empty set (`strategies: []`, `flags: ["empty_set"]`).

   The system prompt also embeds five worked few-shot calibration examples
   (bare greeting, multi-strategy stacking, overhead/statistics combo,
   a four-label turn, and incremental-ask vs. persistent-repetition) to
   anchor edge-case judgment before any real batch is seen.

2. **Batch user prompt** (`prompt.md`, Section 3) — a fixed instruction
   wrapper naming the required output fields (`turn_id`, `dialogue_id`,
   `turn_index`, `strategies`, `categories`, `n_labels`, `flags`, `note`,
   `text`) followed by the batch's 200-turn JSON payload pasted verbatim.

`pipeline.py`'s `build-prompts` step reconstructs exactly this pair of
documents per batch, so the literal text sent for any batch can be
regenerated and reviewed.

## 5. Step 4 — Labeling (batch-by-batch, one at a time)

Labeling follows a fixed protocol (`prompt.md`, Section 5):

1. **Smoke test on the first batch of a run.** The first batch is
   annotated first and in isolation, producing the full annotated JSON
   array plus a short summary (strategy frequency, empty-set count,
   notable edge cases).
2. **Manual verification checkpoint.** Annotation stops after that first
   batch and explicitly waits for sign-off before continuing — this is the
   single quality gate on the whole run: if the taxonomy, the Removal
   Test, or the output schema were being misapplied, it gets caught here
   before propagating across the rest of the run.
3. **Sequential run, remaining batches.** After approval, the remaining
   batches are processed one at a time, each producing its own complete
   `annotated_batch/batch_NN_annotated.json` file with the same schema.

**Important methodological note:** annotation is performed by directly
driving an LLM agent (Claude) in an interactive session, reading each batch
and reasoning through it against the taxonomy and decision tests — **not**
via a scripted call to a model API in a loop. There is no batch-level
temperature/sampling parameter or API request log to point to; the
"annotator" is the agent's own reasoning over the fixed prompt, batch by
batch, under the human checkpoint described above. `pipeline.py` represents
this step with an explicit `AnnotatorClient` seam (raises rather than
fabricates output) precisely so this distinction stays visible to a
reviewer rather than being implied away by having a script "run" it.

Each output turn object records:
- the selected `strategies` and their parent `categories`,
- `n_labels` (redundant count, used for the density-cap check),
- `flags` (only `empty_set` is used in practice),
- a `note` field containing a short Chain-of-Thought: which phrase
  triggered each strategy, why it survives the Removal Test, and why a
  plausible alternative label was excluded.

## 6. Step 5 — Validation

Each annotated batch is checked against:
- **Schema completeness** — all required fields present.
- **Closed-world taxonomy** — every string in `strategies` must be one of
  the 41 defined strategies.
- **Category consistency** — `categories` must equal exactly the set of
  parent categories implied by `strategies`.
- **Label-count consistency** — `n_labels == len(strategies)`, capped at 6.
- **Empty-set convention** — `n_labels == 0` must carry the `empty_set`
  flag.

`pipeline.py`'s `validate` step automates this check across whatever batches
are present in `annotated_batch/`. Any off-taxonomy strategy strings,
missing files, or schema mismatches are reported explicitly rather than
silently absorbed, so drift introduced in a later batch (i.e. not caught by
a first-batch-style checkpoint) surfaces before the data is used downstream.

## 7. Step 6 — Merging into final deliverables

Once all batches in a run are annotated, they are concatenated in batch
order into three final artifacts:

| File | Format |
| --- | --- |
| `*.jsonl` | one JSON object per line, full schema |
| `*.csv` | same data flattened; `strategies`/`categories`/`flags` pipe-joined into single string columns |
| `*_wide.csv` | one-hot matrix: 41 `has_<strategy>` + 11 `cat_<category>` binary columns per turn, for downstream statistical/ML use |

## 8. Step 7 — Summary statistics

A `SUMMARY.md` is generated from the merged data: turn/dialogue counts,
labels-per-turn distribution (mean/median/std. dev.), empty-set rate, and
per-category / per-strategy prevalence tables. This is the standard
sanity-check view used to spot skew (e.g. which strategies dominate vs.
which are rare-to-unused in a given slice) before the data is used for
downstream modeling.

---

## End-to-end flow (for presentation)

```
persuader_turns.csv (target row range)
        |
        v
[1] SLICE into fixed-size batches                -> batch/batch_NN_turns_X_Y.json
        |  (context = last 5 turns, pre-embedded per row)
        v
[2] ASSEMBLE prompt per batch                     -> system prompt (prompt.md) + batch user prompt
        |
        v
[3] LABEL one batch at a time                     -> annotated_batch/batch_NN_annotated.json
        |  First batch = smoke test -> manual sign-off -> remaining batches sequential
        v
[4] VALIDATE against schema + closed-world taxonomy
        |
        v
[5] MERGE all batches                             -> <run>.jsonl, <run>.csv, <run>_wide.csv
        |
        v
[6] SUMMARIZE                                     -> SUMMARY.md
```

`pipeline.py` implements steps [1], [2], [4], [5], and [6] as runnable code
and represents step [3] with an explicit, documented seam — reflecting that
labeling itself is done by direct agent reasoning under a human checkpoint,
not a scripted model call.
