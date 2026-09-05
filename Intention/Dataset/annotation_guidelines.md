# Donation Intent Annotation Guidelines

## Task

This protocol defines the labeling procedure for dialogues from the Persuasion-For-Good
corpus. In each dialogue, one person (the **Persuader**) tries to convince the other
person (the **Persuadee**) to donate part of their task payment to a children's
charity. Annotators read each dialogue and label **what the Persuadee actually
committed to**, based only on what the Persuadee says in the text.

## Why manual labels

The dataset's existing numeric fields (`intended`, `donation_ee`) do not always match
what's said in the dialogue. For example, one conversation has the Persuadee clearly
agreeing ("we have you down for a $10 donation. Is that correct?" / "yes that is" /
"yes thats ok") but the recorded `donation_ee` is $0. In another, the Persuadee says
"I will absolutely look to donating something later" but both numeric fields show $0.
These gaps are exactly what the manual labels are meant to fix.

## Labels

Each dialogue gets two fields:

### 1. `binary_label` (required): `yes` or `no`

- **`yes`** — the Persuadee makes an unconditional, unqualified commitment to donate
  (any amount greater than $0) as part of *this* task/transaction.
- **`no`** — the Persuadee does not make such a commitment. This includes explicit
  refusals, never actually answering the ask, selecting/stating $0, and conditional
  or deferred cases that never resolve into a firm commitment within this
  conversation.

### 2. `modifier` (required, but often blank/null): `conditional`, `deferred`, or blank

- **`conditional`** — the Persuadee ties their willingness to donate to some
  condition that is never confirmed or met (e.g., "I'll donate $2 if you promise
  none of it goes to X" and the Persuader never confirms X).
- **`deferred`** — the Persuadee expresses genuine intent to donate, but later, or
  outside this task (e.g., "I'll look at the website with my daughter and donate
  there," "I'll consider it after this survey").
- **Blank/null** — neither applies. Explicitly consider this field for every row —
  don't just skip it. A clean "yes" and a clean "no" both get a blank modifier.

## Worked examples

| What the Persuadee says | binary_label | modifier |
|---|---|---|
| "Yes, $10 sounds good, go ahead and charge me." | `yes` | (blank) |
| "No thanks, I'm not interested in donating." | `no` | (blank) |
| "I'll donate $0 today." | `no` | (blank) |
| "I'd donate $2 if you can guarantee it goes to local kids." (Persuader never confirms) | `no` | `conditional` |
| "I'll check out their website later and maybe donate there." | `no` | `deferred` |
| "Sure, I'll donate $1 now, and I might give more later too." | `yes` | `deferred` |

## Rules of thumb

1. **Only use what the Persuadee explicitly says.** Don't infer intent from tone,
   politeness, or what you think they'd "probably" do.
2. **Use the Persuadee's last clear position**, if it changes during the
   conversation. People often start skeptical and warm up, or start receptive and
   back out — go with where they land.
3. **The Persuader's own claims about donating don't count.** Only the Persuadee's
   stated commitment matters for these labels.
4. **If the Persuadee never gives a clear answer either way** (conversation ends
   without a resolution), label it `no` with a blank modifier — no commitment was
   made.

## Data location

Corpus files: `persuasionforgood_corpus/` (ConvoKit export)
- `conversations.json` — one entry per dialogue, keyed by conversation id.
- `utterances.jsonl` — one line per utterance; `root` matches the conversation id;
  `meta.role` is `0` for Persuader and `1` for Persuadee.

Annotators do not need to touch these files directly — each assigned batch file
(`annotations_<name>.xlsx`) already has the full dialogue text rendered in the
`dialogue_text` column, with each line prefixed `[Persuader]` or `[Persuadee]`.

## Annotation file format

Each annotator works from an Excel file, `annotations_<name>.xlsx`, containing 50
rows and the following columns:

- `conversation_id`, `dialogue_id` — identifiers; leave unchanged
- `dialogue_text` — the full conversation to be read
- `binary_label` — select `yes` or `no` from the cell dropdown
- `modifier` — select `conditional`, `deferred`, or leave blank from the cell
  dropdown

Both label columns have built-in dropdown menus (a small arrow appears when the
cell is selected). Dropdown selections should be used instead of free text entry,
so labels stay consistent across annotators.

`binary_label` and `modifier` should be completed for all 50 rows before the file
is returned.
