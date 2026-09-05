# Merged phase-1 multi-label persuasion-strategy dataset

Turn-level manual annotation of the **first 10,600 persuader turns** of
`../persuader_turns.csv` with the 41-strategy / 11-category multi-label taxonomy
(`../taxonomy_multilabel.json`, `../guideline_multi_strategy.md`). Every persuader
turn is labelled with the *set* of persuasion strategies it uses (possibly empty).

The turns come from the P4G ("Persuasion For Good") donation-solicitation dialogues:
a *persuader* tries to convince a *persuadee* to donate part of their task
earnings to Save the Children. Only persuader turns are annotated.

## Contents

| File | Description |
| --- | --- |
| `multilabel_merged.jsonl` | one JSON object per turn - primary format |
| `multilabel_merged.csv` | same rows, flat; list columns are `\|`-separated |
| `multilabel_merged_wide.csv` | 10,600 x 56 binary matrix: ids + 41 `has_*` + 11 `cat_*` |
| `eda/STATS.md` | full statistics, overall and per annotator |
| `eda/*.png` | 14 EDA figures (see below) |
| `eda/*.csv` | machine-readable stat tables |
| `build_merge.py` | reproduces the three data files from the source segments |
| `build_eda.py` | reproduces everything under `eda/` |

## How it was assembled

The four annotation segments were produced independently by different people /
runs. They are concatenated here in the canonical row order of
`persuader_turns.csv` (which is also global turn order):

| Order | Annotator | Turn range | Turns | Source folder |
| --- | --- | --- | --- | --- |
| 1 | shimanto | 1 – 2000 | 2,000 | `../annotation_first_2000_shimanto/` |
| 2 | shovon | 2001 – 4000 | 2,000 | `../annotation_shovon/` |
| 3 | *unassigned* | 4001 – 6000 | 2,000 | `../annotation_turns_4001_6000/` (`model_id = claude-opus-3.7-batch`) |
| 4 | shovon | 6001 – 7000 | 1,000 | `../annotation_shovon/` |
| 5 | abhishek | 7001 – 10600 | 3,600 | `../annotation_7001_10600_abhishek/` |

`shovon`'s folder holds one merged file covering both of its ranges (2001–4000
and 6001–7000); the build script slices it back into the right positions. The
4001–6000 segment has no annotator name anywhere in the source tree and its
records carry `model_id = claude-opus-3.7-batch`, so it is recorded as
`unassigned`.

During the merge, each record's `categories` are **recomputed from its
`strategies`** via the taxonomy, so strategy-level and category-level views can
never disagree. No zero adjustments were needed - the source categories already
matched.

## Schema (`multilabel_merged.jsonl`)

| Field | Type | Notes |
| --- | --- | --- |
| `global_index` | int | 0-based position in canonical order (= row in `persuader_turns.csv`) |
| `turn_id` | str | `{dialogue_id}#t{turn_index}` |
| `dialogue_id` | str | P4G dialogue identifier |
| `turn_index` | int | 0-based turn index *within the full dialogue* (persuadee turns included, hence even numbers dominate) |
| `conversation_id` | str | P4G numeric conversation id |
| `persuader_turn_index` | str | 0-based index among *persuader* turns of the dialogue |
| `n_turns_in_dialogue` | str | total turns in the source dialogue |
| `annotator` | str | `shimanto` \| `shovon` \| `unassigned` \| `abhishek` |
| `strategies` | list[str] | 0–6 strategy names from the taxonomy |
| `categories` | list[str] | parent categories of `strategies`, taxonomy order |
| `n_labels` | int | `len(strategies)` |
| `flags` | list[str] | `empty_set` marks a deliberate no-strategy turn (greetings, acks) |
| `note` | str | annotator's chain-of-thought / justification (may be empty) |
| `text` | str | the persuader utterance |

The wide CSV column order is fixed by the taxonomy: strategies grouped by
category (`has_logical_appeal … has_rapport_building`), then the 11
`cat_*` columns.

## Dataset at a glance

- **10,600 turns** across **1,017 dialogues** (mean 10.4 annotated persuader turns/dialogue).
- **Mean 1.68 strategies per turn**, median 1; **6.7 % empty**, **48.9 % multi-label**, max 6.
- All **41 strategies** and all **11 categories** occur.
- Dominant categories: *Relational and Interactive* (46 %), *Information Provision* (36 %),
  *Emotional Appeal* (16 %). Rare: *Urgency and Scarcity*, *Commitment and Consistency*,
  *Threat and Pressure* (each < 3 %).
- Top strategies: `rapport_building` (27 %), `organization_information` (16 %),
  `donation_procedure_information` (13 %), `personal_related_inquiry` (13 %),
  `personal_story` (11 %).
- **Annotator effect:** label density differs sharply by segment - shimanto
  ~2.38 strategies/turn, shovon ~1.78, unassigned ~1.61, abhishek ~1.24. This is
  a labelling-granularity difference, not a property of the conversations. Treat
  `annotator` as a batch/rater variable in any downstream modelling or
  agreement analysis.

Full numbers (per-turn label histogram, category & strategy prevalence overall
and per annotator, top strategies per segment) are in [`eda/STATS.md`](eda/STATS.md).

## EDA figures (`eda/`)

| # | File | Shows |
| --- | --- | --- |
| 01 | `01_labels_per_turn.png` | distribution of strategies per turn |
| 02 | `02_category_prevalence.png` | % of turns using each category |
| 03 | `03_strategy_prevalence.png` | % of turns using each of the 41 strategies, coloured by category |
| 04 | `04_category_cooccurrence.png` | how often two categories share a turn |
| 05 | `05_strategy_cooccurrence_top20.png` | pairwise co-occurrence of the 20 commonest strategies |
| 06 | `06_label_density_by_segment.png` | mean labels/turn and empty-set rate per annotator |
| 07 | `07_nlabels_violin_by_segment.png` | full label-count distribution per annotator |
| 08 | `08_category_by_segment.png` | category prevalence (%) per annotator |
| 09 | `09_strategy_by_position.png` | selected strategies vs. normalised position in the dialogue |
| 10 | `10_label_density_along_corpus.png` | rolling mean labels/turn along global index, segment boundaries marked |
| 11 | `11_dialogue_and_text_length.png` | turns per dialogue; words per turn |
| 12 | `12_flags.png` | flag counts |
| 13 | `13_strategy_rank_frequency.png` | Zipf-style rank/frequency of strategies |
| 14 | `14_strategy_correlation.png` | phi-correlation between strategy indicators |

Key reading: **04** and **14** show that persuaders bundle *Relational /
Information* moves with *Emotional* and *Social* appeals rather than with cold
*Rational* arguments; **09** shows `rapport_building` and inquiries front-loaded
while `donation_procedure_information` and `persistent_repetition` rise toward
the end; **10** makes the per-annotator density shift impossible to miss.

## Regenerating

```bash
cd merged_dataset
python build_merge.py     # -> multilabel_merged.{jsonl,csv} + _wide.csv
python build_eda.py       # -> eda/
```
Requires `pandas`, `numpy`, `matplotlib`, `seaborn`.

---

## Five worked examples

Each turn is annotated with the *set* of strategies present. Use the "removal
test": a label stays only if removing that span from the utterance would remove
that persuasive function.

### 1. Empty set — a bare greeting

> **Text:** "Good morning"
> **Turn:** `20180831-063536_532_live#t000` (global_index 0, shimanto)
> **Strategies:** `[]`  ·  **Flags:** `empty_set`

The opening turn of the dialogue. A pleasantry with no donation-directed
content carries no strategy. The taxonomy reserves `rapport_building` for
*substantive* relationship work (small talk about the other person, shared
experience), not reflexive politeness, so this is a deliberate empty set rather
than a missing label. About 6.7 % of turns are like this.

### 2. Single label — relationship maintenance

> **Text:** "i am pleasure for my charity, all the best for you"
> **Turn:** `20180823-020542_443_live#t014` (global_index 2002, shovon)
> **Strategies:** `rapport_building` → *Relational and Interactive*

"all the best for you" is a warmth-building move directed at the persuadee - it
invests in the interpersonal relationship without giving information, making an
argument, or applying pressure. Only that one function is present, so it is a
clean single-label turn. `rapport_building` is the single most common strategy in
the corpus (27 % of turns).

### 3. Two labels — minimization + logic ("coffee money")

> **Text:** "We could all do better, I suppose. These organizations only ask for a
> small amount that we may spend on coffee each day or snacks we don't need."
> **Turn:** `20180826-064412_288_live#t006` (global_index 3122, shovon)
> **Strategies:** `minimization_framing`, `logical_appeal`
> → *Framing and Presentation*, *Rational Appeal*

Two distinct functions in one sentence:
- **`minimization_framing`** — "only ask for a small amount" reframes the ask as
  trivially small.
- **`logical_appeal`** — "money we'd spend on coffee / snacks we don't need"
  is a reasoned equivalence: you already spend this much on things of no value,
  therefore redirecting it costs you nothing real.

Remove the "small amount" phrase and the reasoning survives; remove the
coffee/snacks comparison and the minimization survives. Both labels are
independently licensed. This *minimization + rational* pairing is one of the
commonest strategy combinations in the data.

### 4. Two labels — comparison framing under pressure

> **Text:** "are you sure, i mean how much money do they spend on unnecessary
> stuff like a bag of snack or candy?"
> **Turn:** `20180828-220746_854_live#t012` (global_index 117, shimanto)
> **Strategies:** `comparison_framing`, `persistent_repetition`
> → *Framing and Presentation*, *Threat and Pressure*

- **`comparison_framing`** — the donation is set against "a bag of snack or
  candy", anchoring it to a negligible everyday purchase. (Contrast with example
  3: here it is an explicit *comparison* to a named alternative, not just "it's
  small".)
- **`persistent_repetition`** — "are you sure" re-opens the ask *after the
  persuadee has already declined*. Re-pressing a refused request is a pressure
  move, hence the *Threat and Pressure* category even though the tone stays
  polite.

Context matters for the second label: the same words earlier in a dialogue,
before any refusal, would not be `persistent_repetition`.

### 5. Four labels — a dense, layered turn

> **Text:** "That's rough. I totally feel you there. I'm on short-term disability
> and receiving money from the union, insurance, and people from the jobsite. The
> way I look at it is I am not donating that assistance, I'm donating my time. If
> I earn a buck for a turk for a minute, and I donate a few cents, then I'm not
> using the money people gave me, just my free time."
> **Turn:** `20180828-171020_885_live#t018` (global_index 207, shimanto)
> **Strategies:** `rapport_building`, `personal_story`, `logical_appeal`,
> `minimization_framing`
> → *Relational and Interactive*, *Rational Appeal*, *Framing and Presentation*

Four functions stacked in one turn:
- **`rapport_building`** — "That's rough. I totally feel you there." acknowledges
  the persuadee's stated hardship and aligns with them.
- **`personal_story`** — the speaker's own disability / income situation, a
  concrete first-person narrative.
- **`logical_appeal`** — the argument that donating a few cents earned per minute
  means "donating my time", not spending the assistance money others gave them.
- **`minimization_framing`** — "a few cents" frames the contribution as
  negligible.

Each survives the removal test on its own. Turns with 4+ labels are only ~6 % of
the corpus and cluster in the shimanto segment, which was annotated at finer
granularity - a good illustration of why `annotator` should be carried as a
covariate.
