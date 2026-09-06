# Donation Intent Annotation Guidelines (v2 — strict binary)

## Task

This protocol defines the labeling procedure for dialogues from the Persuasion-For-Good
corpus. In each dialogue, one person (the **Persuader**) tries to convince the other
person (the **Persuadee**) to donate part of their task payment to a children's
charity. Annotators read each dialogue and label **whether the Persuadee made a fully
clear, unconditional commitment to donate**, based only on what the Persuadee says in
the text.

## Why manual labels

The dataset's existing numeric fields (`intended`, `donation_ee`) do not always match
what's said in the dialogue. For example, one conversation has the Persuadee clearly
agreeing ("we have you down for a $10 donation. Is that correct?" / "yes that is" /
"yes thats ok") but the recorded `donation_ee` is $0. These gaps are exactly what the
manual labels are meant to fix.

## What changed in this revision

The original scheme (see `Dataset/annotation_guidelines.md`, kept for legacy reference)
used two fields — `binary_label` (`yes`/`no`) plus a `modifier` (`conditional`,
`deferred`, or blank) that let a dialogue be labeled `yes` even when the commitment
carried a hedge (e.g., a firm amount now plus a vague maybe-more-later remark).

Per supervisor direction, the `modifier` field is **removed**. There is now a single
field, and the bar for `yes` is stricter:

> **If the Persuadee's stated intention is not a 100% clear, unconditional "yes," it is
> a `no`.** Any hesitation, condition, partial commitment, or deferral to a later time —
> any "if," "but," "maybe," "I'll think about it," or similar — makes the answer `no`,
> even if part of the same statement also contains a firm commitment.

Concretely, every dialogue previously labeled `yes` **and** carrying a `conditional` or
`deferred` modifier was initially relabeled `no`. Only dialogues that were `yes` with
**no** modifier stayed `yes`. This first pass was a direct, deterministic remapping of
the existing `binary_label` + `modifier` pairs — no dialogue text was read at this
stage, since the modifier field already recorded exactly which `yes` cases carried a
hedge somewhere in the conversation.

| Old `binary_label` | Old `modifier` | Pass-1 `binary_label` |
|---|---|---|
| `yes` | (blank) | `yes` |
| `yes` | `conditional` | `no` |
| `yes` | `deferred` | `no` |
| `no` | (blank) | `no` |
| `no` | `conditional` | `no` |
| `no` | `deferred` | `no` |

That deterministic pass produced 657 `yes` / 360 `no` (81 dialogues moved from `yes`
to `no`, down from 738 `yes` / 279 `no` under the old two-field scheme).

**Pass 2 — manual re-check of the 81 flips.** A modifier tag records that a hedge
appeared *somewhere* in the dialogue, not that the hedge was still standing by the time
the conversation ended. So all 81 dialogues that moved from `yes` to `no` were read in
full by hand and checked against rule of thumb #2 below (use the Persuadee's *last
clear position*). In many of them the hedge the old annotator flagged had already been
resolved earlier in the conversation, and the dialogue went on to end in a clean,
unhedged commitment that the modifier tag was never updated to reflect.

Of the 81: **44 were confirmed correctly `no`** (the hedge or non-commitment genuinely
stands at the end of the dialogue), and **37 were reverted back to `yes`** (the
Persuadee's actual final position was unhedged, even though an earlier turn had
triggered the old `conditional`/`deferred` tag). The full per-dialogue reasoning and
dialogue text for all 81 is in
[`flip_recheck_report.md`](flip_recheck_report.md).

**Final distribution: 694 `yes` / 323 `no`** across 1,017 dialogues.

## Labels

Each dialogue gets a single field:

### `binary_label` (required): `yes` or `no`

- **`yes`** — the Persuadee makes a fully clear, unconditional, unqualified commitment
  to donate (any amount greater than $0) as part of *this* task/transaction, with no
  hedging attached to that commitment.
- **`no`** — everything else. This includes explicit refusals, never actually
  answering the ask, selecting/stating $0, conditional commitments (tied to something
  the Persuader never confirms), deferred intentions (donating later or outside this
  task), and any commitment qualified by hesitation ("maybe," "I might," "I'll think
  about it," "probably," "if I have time," etc.) — even when a specific amount is also
  mentioned in the same breath.

## Worked examples

| What the Persuadee says | binary_label |
|---|---|
| "Yes, $10 sounds good, go ahead and charge me." | `yes` |
| "No thanks, I'm not interested in donating." | `no` |
| "I'll donate $0 today." | `no` |
| "I'd donate $2 if you can guarantee it goes to local kids." (Persuader never confirms) | `no` |
| "I'll check out their website later and maybe donate there." | `no` |
| "Sure, I'll donate $1 now, and I might give more later too." | `no` |
| "Okay, I guess I could give a dollar." | `no` |
| "Absolutely, take $2 from my payment." | `yes` |

Note the fifth-from-last example: under the previous scheme this was `yes` +
`deferred` because the $1-now portion was unconditional. Under this revision, the
hedge on the *same statement* ("I might give more later") is enough to make the whole
answer `no` — this is the central behavior change from v1.

## Rules of thumb

1. **Only use what the Persuadee explicitly says.** Don't infer intent from tone,
   politeness, or what you think they'd "probably" do.
2. **Use the Persuadee's last clear position**, if it changes during the
   conversation. People often start skeptical and warm up, or start receptive and
   back out — go with where they land.
3. **The Persuader's own claims about donating don't count.** Only the Persuadee's
   stated commitment matters for this label.
4. **When in doubt, label `no`.** The bar for `yes` is a clean, unhedged, resolved
   commitment. Any ambiguity, partial resolution, or mixed signal defaults to `no`.
5. **If the Persuadee never gives a clear answer either way** (conversation ends
   without a resolution), label it `no` — no commitment was made.

## Data location

Corpus files: `persuasionforgood_corpus/` (ConvoKit export)
- `conversations.json` — one entry per dialogue, keyed by conversation id.
- `utterances.jsonl` — one line per utterance; `root` matches the conversation id;
  `meta.role` is `0` for Persuader and `1` for Persuadee.

Two dataset files, both dialogue-consistent with each other (same `binary_label` per
`dialogue_id` in both):

- `Dataset_updated/donation_intetion_manual_label_dataset.csv` — one row per
  **Persuader** turn (10,600 rows across 1,017 dialogues), with `text` (the turn
  itself), `context` (up to 5 prior turns, rendered with `[Persuader]`/`[Persuadee]`
  tags), and `binary_label` (dialogue-level, repeated on every turn row for that
  dialogue).
- `Dataset_updated/Manual_Label.csv` — one row per **dialogue** (1,017 rows), with the
  **complete** dialogue transcript in `dialogue_text` (both speakers, start to finish)
  and `binary_label`.

⚠️ **If you need to re-read a dialogue's actual ending, use `Manual_Label.csv`, not the
turn-level file.** The turn-level file only stores **Persuader** turns as rows; a
dialogue's true final line is very often a **Persuadee** turn, and when that's the
case it does not appear anywhere in the turn-level file — not as `text`, and not as
`context` on a later row, because there is no later Persuader row to carry it. (This
affects the majority of dialogues here, since the Persuadee's donation decision is
usually the last thing said.) `Manual_Label.csv`'s `dialogue_text` always has the full
conversation and is the file all 81 dialogues in `flip_recheck_report.md` were
actually re-read from.

## Annotation file format

Each annotator works from an Excel file, `annotations_<name>.xlsx`, containing 50
rows and the following columns:

- `conversation_id`, `dialogue_id` — identifiers; leave unchanged
- `dialogue_text` — the full conversation to be read
- `binary_label` — select `yes` or `no` from the cell dropdown

The label column has a built-in dropdown menu (a small arrow appears when the cell is
selected). Dropdown selections should be used instead of free text entry, so labels
stay consistent across annotators.

`binary_label` should be completed for all 50 rows before the file is returned.
