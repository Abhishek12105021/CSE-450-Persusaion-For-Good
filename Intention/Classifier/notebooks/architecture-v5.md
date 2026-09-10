# MAPL Capstone — Donation-Intent Classifier, Architecture v5

This documents `capstone-v5-augfix.ipynb`, a fork of v4
(`capstone-v4-focal-contrastive.ipynb` — see
[architecture-v4.md](architecture-v4.md)). Model, loss, and training loop
are unchanged from v4. **The only change is the EDA augmentation step.**

**Trigger:** a teammate reported that v3's augmentation "wasn't working
properly." It was carried into v4 unchanged, so the same bug was live
there too. Reading the code and running it against the actual labeled
dataset (`dataset-persuassion/Manual_Label.csv`, 1017 rows) turned up a
concrete, measurable defect plus a reproducibility bug.

---

## 1. What was actually broken

### Bug 1 — marker corruption (the main one)

v3/v4 tokenize dialogue text with `text.split(" ")` and "protect"
`[Persuader]`/`[Persuadee]` markers from being touched by checking
`token.strip(punct).lower() in {"[persuader]", "[persuadee]"}`. That only
works if the marker is its own space-delimited token.

Checked against the real corpus:

```
total marker occurrences:                 20,932
glued to the preceding char (no space):    12,030   (57.5%)
```

Most markers in this dataset are glued directly to a preceding `\n` with
no space (e.g. `"...today?\n[Persuadee] Hi..."`), so
`text.split(" ")` produces a single token like `"today?\n[Persuadee]"`.
That token is not equal to `"[persuadee]"` after stripping punctuation, so
the protection check silently fails for the majority of markers — the
swap and delete augmentation ops then treat the glued marker as an
ordinary word, free to delete or shuffle.

Measured impact: running the real augmentation function against every
training row, **15.9% of augmented variants ended up with a different
`[Persuader]`/`[Persuadee]` marker count than their source row** — i.e.
roughly 1 in 6 synthetic training examples had its turn structure
corrupted, sometimes losing a marker and the first few words of that
turn together in a single deletion pass. Example (before → after):

```
ORIG: "[Persuader] Hello, how are you?\n[Persuadee] I'm doing well, a little tired. How are you?\n[Persuader] I am fine..."
AUG : "[Persuader] Hello, how are I'm doing well, a little How are you?\n[Persuader] am fine thank..."
```

(The `[Persuadee]` marker and "tired." both vanished in the same
deletion pass.)

This mattered more than a generic augmentation bug would, because
`conditional` and `deferred` rows get the *heaviest* augmentation (6x and
2x extra copies respectively) — the classes this whole augmentation step
exists to help were the most exposed to it. It also feeds the
speaker-role embedding: `compute_batch_role_ids()` (unchanged) reads
these exact markers at train time, so a corrupted marker on an augmented
row can also scramble that row's role-id assignment, not just its text.

### Bug 2 — non-reproducible seeding

Each augmented copy was seeded with `seed=hash((row["text"], k)) % (2**31)`.
Python randomizes string `hash()` per process by default
(`PYTHONHASHSEED`) — confirmed locally: hashing the same string in three
separate `python -c` invocations gave three different numbers. So despite
`CONFIG["SEED"] = 42` being threaded through `random`/`numpy`/`torch`
elsewhere, the augmented *text itself* silently differed on every kernel
restart.

---

## 2. What's fixed in v5

| # | Fix | Detail |
|---|---|---|
| 1 | Marker-safe tokenizer | `text.split(" ")` → regex `\[Persuader\]\|\[Persuadee\]\|\S+`, which matches a marker as its own atomic token first regardless of what it's glued to. Verified: 0/3051 sampled augmented variants have a marker-count mismatch after the fix (down from 15.9%). The notebook's new cell 3c runs this exact check live, against the actual post-augmentation `train_df`. |
| 2 | Deterministic seeding | `hash((text, k))` → `hashlib.sha256`-based stable seed. Verified reproducible across separate process invocations. |
| 3 | Persuadee-turn-biased perturbation (new, not a bug fix) | Per `guideline.md`, every label is defined entirely by what the Persuadee says. Synonym replacement and insertion now prefer Persuadee-turn tokens (`CONFIG["aug_persuadee_bias_weight"] = 0.75`) instead of picking uniformly across the whole dialogue including Persuader small talk. Swap and deletion are left role-agnostic — they're structural noise, not phrasing diversity, and restricting their candidate pool further would hurt already-short `conditional` dialogues. |

Nothing else about the augmentation changed: same per-class multipliers
(`aug_num_conditional=6`, `aug_num_deferred=2`, `aug_num_no=1`), same
`aug_alpha=0.15`, same protected-word list, same synonym table, same
four operation types (synonym / swap / delete / insert). Those ratios
were already producing the documented counts correctly
(conditional 9→63 rows, deferred 47→141 rows on this split) — only the
*text-level* correctness of what gets produced was broken.

---

## 3. Everything else

Model architecture, loss (class-balanced focal + supervised contrastive),
cascaded modifier head, attention pooling, binary-macro-F1 checkpoint
selection, the 70/15/15 stratified split, threshold tuning, the
3-encoder sweep, and all reporting/plots are identical to v4 — see
[architecture-v4.md](architecture-v4.md) for those. Outputs are suffixed
`_v5` and checkpoints go to `checkpoints_v5/`, so this can run in the same
working directory as v3 and v4 without overwriting their artifacts.

---

## 4. Known remaining limitation

Unchanged from v3/v4: `conditional` has only ~9-13 real training examples
pre-augmentation. This fork fixes *how* those examples get perturbed — it
does not create new information. If `conditional` is still the weak point
after this run, the durable fix is still more labeled `conditional`
examples; the next cheapest thing to try from the README is ensembling
the 3 already-trained encoders' probabilities (idea #6).
