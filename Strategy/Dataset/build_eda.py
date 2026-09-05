"""
EDA for the merged phase-1 multi-label persuasion-strategy dataset.

Reads   multilabel_merged.jsonl  (+ taxonomy)
Writes  eda/*.png                figures
        eda/STATS.md             full statistics (overall + per-annotator, in the
                                 style of the shimanto / abhishek SUMMARY.md files)
        eda/*.csv                machine-readable stat tables
"""
import json, textwrap
from pathlib import Path
from itertools import combinations
import collections

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EDA  = HERE / "eda"
EDA.mkdir(exist_ok=True)

TAX = json.loads((ROOT / "taxonomy_multilabel.json").read_text(encoding="utf-8"))
STRATS, STRAT2CAT = [], {}
for cat, cv in TAX["categories"].items():
    for s in cv["strategies"]:
        STRATS.append(s); STRAT2CAT[s] = cat
CATS = list(TAX["categories"].keys())

# ---------------------------------------------------------------- load
recs = [json.loads(l) for l in (HERE / "multilabel_merged.jsonl").open(encoding="utf-8")]
df = pd.DataFrame(recs)
df["strategies"] = df["strategies"].apply(list)
df["categories"] = df["categories"].apply(list)
df["flags"] = df["flags"].apply(list)
df["n_cats"] = df["categories"].apply(len)
df["text_len"] = df["text"].fillna("").str.split().apply(len)

SEG_ORDER = ["shimanto", "shovon", "unassigned", "abhishek"]
SEG_RANGE = {"shimanto": "turns 1-2000", "shovon": "turns 2001-4000 + 6001-7000",
             "unassigned": "turns 4001-6000", "abhishek": "turns 7001-10600"}

# ---------------------------------------------------------------- style
sns.set_theme(style="whitegrid", font_scale=0.9)
PAL = "#4C72B0"
CATPAL = sns.color_palette("tab20", len(CATS))
CATCOLOR = dict(zip(CATS, CATPAL))
plt.rcParams["figure.dpi"] = 110
plt.rcParams["savefig.bbox"] = "tight"
plt.rcParams["axes.titleweight"] = "bold"


def save(fig, name):
    fig.savefig(EDA / name, dpi=130)
    plt.close(fig)
    print("  figure:", name)


# ---------------------------------------------------------------- stat helpers
def strat_counts(sub):
    c = collections.Counter()
    for row in sub["strategies"]:
        c.update(row)
    return c


def cat_counts(sub):
    c = collections.Counter()
    for row in sub["categories"]:
        c.update(row)
    return c


def overview(sub):
    n = len(sub)
    tpd = sub.groupby("dialogue_id").size()
    nl = sub["n_labels"]
    return {
        "turns": n,
        "dialogues": sub["dialogue_id"].nunique(),
        "turns_per_dialogue_mean": round(tpd.mean(), 2),
        "turns_per_dialogue_min": int(tpd.min()),
        "turns_per_dialogue_max": int(tpd.max()),
        "mean_labels_per_turn": round(nl.mean(), 3),
        "median_labels_per_turn": float(nl.median()),
        "std_labels_per_turn": round(nl.std(), 3),
        "empty_set_turns": int((nl == 0).sum()),
        "empty_set_pct": round(100 * (nl == 0).mean(), 1),
        "max_labels_on_a_turn": int(nl.max()),
        "distinct_strategies_used": len(strat_counts(sub)),
        "distinct_categories_used": len(cat_counts(sub)),
        "multi_label_pct": round(100 * (nl >= 2).mean(), 1),
    }


# ================================================================ STATS.md
md = []
md.append("# Merged phase-1 dataset - EDA & statistics\n")
md.append(textwrap.dedent(f"""\
    Manual multi-label persuasion-strategy annotation of the **first 10,600 persuader turns**
    of `persuader_turns.csv` ({len(STRATS)} strategies / {len(CATS)} categories, see
    `taxonomy_multilabel.json` and `guideline_multi_strategy.md`).

    Built by concatenating four independently-produced annotation segments in canonical
    `persuader_turns.csv` order:

    | Order | Annotator | Range | Turns | Source folder |
    | --- | --- | --- | --- | --- |
    | 1 | shimanto | turns 1-2000 | 2,000 | `annotation_first_2000_shimanto` |
    | 2 | shovon | turns 2001-4000 | 2,000 | `annotation_shovon` |
    | 3 | unassigned | turns 4001-6000 | 2,000 | `annotation_turns_4001_6000` (`model_id = claude-opus-3.7-batch`) |
    | 4 | shovon | turns 6001-7000 | 1,000 | `annotation_shovon` |
    | 5 | abhishek | turns 7001-10600 | 3,600 | `annotation_7001_10600_abhishek` |

    Categories in every record are recomputed from the strategy set via the taxonomy,
    so the strategy/category views are always consistent.
    """))

ov = overview(df)
md.append("## Overview (whole dataset)\n")
md.append("| Metric | Value |\n| --- | --- |")
md.append(f"| Turns | {ov['turns']:,} |")
md.append(f"| Dialogues | {ov['dialogues']:,} |")
md.append(f"| Turns / dialogue | mean {ov['turns_per_dialogue_mean']} "
          f"(min {ov['turns_per_dialogue_min']}, max {ov['turns_per_dialogue_max']}) |")
md.append(f"| Mean labels / turn | {ov['mean_labels_per_turn']} |")
md.append(f"| Median labels / turn | {ov['median_labels_per_turn']} |")
md.append(f"| Std. dev. | {ov['std_labels_per_turn']} |")
md.append(f"| Empty-set turns | {ov['empty_set_turns']:,} ({ov['empty_set_pct']}%) |")
md.append(f"| Multi-label turns (>=2) | {ov['multi_label_pct']}% |")
md.append(f"| Max labels on a turn | {ov['max_labels_on_a_turn']} |")
md.append(f"| Distinct strategies used | {ov['distinct_strategies_used']} / {len(STRATS)} |")
md.append(f"| Distinct categories used | {ov['distinct_categories_used']} / {len(CATS)} |")
md.append("")

# labels per turn
lp = df["n_labels"].value_counts().sort_index()
md.append("## Labels per turn\n")
md.append("| Labels | Turns | % |\n| --- | --- | --- |")
for k, v in lp.items():
    md.append(f"| {k} | {v:,} | {100*v/len(df):.1f} |")
md.append("")

# category prevalence
cc = cat_counts(df)
md.append("## Category prevalence\n")
md.append("| Category | Turns | % |\n| --- | --- | --- |")
for c, n in sorted(cc.items(), key=lambda x: -x[1]):
    md.append(f"| {c} | {n:,} | {100*n/len(df):.1f} |")
md.append("")

# strategy prevalence
sc = strat_counts(df)
md.append("## Strategy prevalence (all 41)\n")
md.append("| Strategy | Category | Turns | % |\n| --- | --- | --- | --- |")
for s in sorted(STRATS, key=lambda s: -sc.get(s, 0)):
    n = sc.get(s, 0)
    md.append(f"| {s} | {STRAT2CAT[s]} | {n:,} | {100*n/len(df):.1f} |")
md.append("")

# per-annotator sections
md.append("## Per-annotator / per-segment statistics\n")
seg_rows = []
for seg in SEG_ORDER:
    sub = df[df["annotator"] == seg]
    o = overview(sub)
    o["annotator"] = seg
    seg_rows.append(o)
    md.append(f"### {seg}  ({SEG_RANGE[seg]})\n")
    md.append("| Metric | Value |\n| --- | --- |")
    md.append(f"| Turns | {o['turns']:,} |")
    md.append(f"| Dialogues | {o['dialogues']:,} |")
    md.append(f"| Turns / dialogue | mean {o['turns_per_dialogue_mean']} "
              f"(min {o['turns_per_dialogue_min']}, max {o['turns_per_dialogue_max']}) |")
    md.append(f"| Mean labels / turn | {o['mean_labels_per_turn']} |")
    md.append(f"| Median labels / turn | {o['median_labels_per_turn']} |")
    md.append(f"| Std. dev. | {o['std_labels_per_turn']} |")
    md.append(f"| Empty-set turns | {o['empty_set_turns']:,} ({o['empty_set_pct']}%) |")
    md.append(f"| Multi-label turns (>=2) | {o['multi_label_pct']}% |")
    md.append(f"| Max labels on a turn | {o['max_labels_on_a_turn']} |")
    md.append(f"| Distinct strategies used | {o['distinct_strategies_used']} / 41 |")
    md.append("")
    top = strat_counts(sub).most_common(8)
    md.append("Top strategies: " + ", ".join(f"`{s}` ({n})" for s, n in top) + "\n")

md.append(textwrap.dedent("""\
    > **Annotation-style note.** The four segments were labelled independently and show
    > clearly different label *densities* - shimanto's segment averages ~2.4 strategies
    > per turn while abhishek's averages ~1.2. This is a labelling-granularity effect, not
    > a property of the conversations, and matters for any model trained on the pooled
    > data or for cross-segment agreement studies. See `flags` for turns the annotators
    > marked as uncertain / edge cases.
    """))

# ---------------------------------------------------------------- stat CSVs
pd.DataFrame(seg_rows).set_index("annotator").to_csv(EDA / "overview_by_annotator.csv")
pd.Series(ov).to_csv(EDA / "overview_overall.csv", header=["value"])
(pd.DataFrame({"strategy": STRATS,
              "category": [STRAT2CAT[s] for s in STRATS],
              "turns": [sc.get(s, 0) for s in STRATS]})
   .assign(pct=lambda d: (100*d.turns/len(df)).round(2))
   .sort_values("turns", ascending=False)
   .to_csv(EDA / "strategy_prevalence.csv", index=False))
(pd.DataFrame({"category": list(cc), "turns": list(cc.values())})
   .assign(pct=lambda d: (100*d.turns/len(df)).round(2))
   .sort_values("turns", ascending=False)
   .to_csv(EDA / "category_prevalence.csv", index=False))

(EDA / "STATS.md").write_text("\n".join(md), encoding="utf-8")
print("wrote eda/STATS.md")

# ================================================================ FIGURES

# 1. labels per turn -------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(lp.index.astype(str), lp.values, color=PAL)
ax.bar_label(bars, fmt="%d", padding=2, fontsize=8)
ax.set(xlabel="strategies assigned to the turn", ylabel="turns",
       title=f"Labels per turn  (mean {ov['mean_labels_per_turn']}, "
             f"{ov['empty_set_pct']}% empty)")
save(fig, "01_labels_per_turn.png")

# 2. category prevalence -------------------------------------------------
cs = pd.Series(cc).sort_values()
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.barh(cs.index, 100*cs.values/len(df), color=[CATCOLOR[c] for c in cs.index])
ax.bar_label(bars, fmt="%.1f%%", padding=3, fontsize=8)
ax.set(xlabel="% of turns", title="Category prevalence")
save(fig, "02_category_prevalence.png")

# 3. strategy prevalence ----------------------------------------------
ss = pd.Series({s: sc.get(s, 0) for s in STRATS}).sort_values()
fig, ax = plt.subplots(figsize=(8, 11))
bars = ax.barh(ss.index, 100*ss.values/len(df),
               color=[CATCOLOR[STRAT2CAT[s]] for s in ss.index])
ax.bar_label(bars, fmt="%.1f%%", padding=3, fontsize=7)
handles = [mpl.patches.Patch(color=CATCOLOR[c], label=c) for c in CATS]
ax.legend(handles=handles, fontsize=7, loc="lower right", title="category")
ax.set(xlabel="% of turns", title="Strategy prevalence (all 41)")
save(fig, "03_strategy_prevalence.png")

# 4. category co-occurrence ------------------------------------------
M = np.zeros((len(CATS), len(CATS)))
ci = {c: i for i, c in enumerate(CATS)}
for row in df["categories"]:
    for a in row:
        for b in row:
            M[ci[a], ci[b]] += 1
co = M.copy()
np.fill_diagonal(co, 0)
fig, ax = plt.subplots(figsize=(9, 7.5))
sns.heatmap(pd.DataFrame(co, index=CATS, columns=CATS), annot=True, fmt=".0f",
            cmap="rocket_r", ax=ax, cbar_kws={"label": "co-occurring turns"})
ax.set_title("Category co-occurrence (same turn)")
save(fig, "04_category_cooccurrence.png")

# 5. top strategy co-occurrence -------------------------------------
top_s = [s for s, _ in sc.most_common(20)]
si = {s: i for i, s in enumerate(top_s)}
Ms = np.zeros((len(top_s), len(top_s)))
for row in df["strategies"]:
    r = [s for s in row if s in si]
    for a, b in combinations(sorted(set(r)), 2):
        Ms[si[a], si[b]] += 1
        Ms[si[b], si[a]] += 1
fig, ax = plt.subplots(figsize=(11, 9))
sns.heatmap(pd.DataFrame(Ms, index=top_s, columns=top_s), annot=True, fmt=".0f",
            cmap="mako_r", ax=ax, cbar_kws={"label": "co-occurring turns"})
ax.set_title("Strategy co-occurrence - top 20 strategies")
save(fig, "05_strategy_cooccurrence_top20.png")

# 6. per-annotator label density -----------------------------------
sd = pd.DataFrame(seg_rows).set_index("annotator").loc[SEG_ORDER]
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
b1 = axes[0].bar(sd.index, sd["mean_labels_per_turn"], color=PAL)
axes[0].bar_label(b1, fmt="%.2f", fontsize=8)
axes[0].set(title="Mean strategies per turn, by segment", ylabel="mean n_labels")
b2 = axes[1].bar(sd.index, sd["empty_set_pct"], color="#C44E52")
axes[1].bar_label(b2, fmt="%.1f%%", fontsize=8)
axes[1].set(title="Empty-set rate, by segment", ylabel="% of turns")
save(fig, "06_label_density_by_segment.png")

# 7. n_labels distribution by segment -----------------------------
fig, ax = plt.subplots(figsize=(8, 4.5))
sns.violinplot(data=df, x="annotator", y="n_labels", order=SEG_ORDER,
               hue="annotator", legend=False, cut=0, palette="Set2", ax=ax)
ax.set(title="Distribution of labels per turn, by segment", xlabel="", ylabel="n_labels")
save(fig, "07_nlabels_violin_by_segment.png")

# 8. category prevalence by segment (heatmap, % within segment) ---
rows = []
for seg in SEG_ORDER:
    sub = df[df["annotator"] == seg]
    cnt = cat_counts(sub)
    rows.append({c: 100*cnt.get(c, 0)/len(sub) for c in CATS})
seg_cat = pd.DataFrame(rows, index=SEG_ORDER)[cs.index[::-1]]
fig, ax = plt.subplots(figsize=(10, 3.6))
sns.heatmap(seg_cat, annot=True, fmt=".0f", cmap="viridis", ax=ax,
            cbar_kws={"label": "% of segment's turns"})
ax.set_title("Category prevalence by segment (%)")
save(fig, "08_category_by_segment.png")

# 9. strategy usage over dialogue position ------------------------
df["pos_bin"] = pd.cut(df["turn_index"] / df.groupby("dialogue_id")["turn_index"].transform("max").clip(lower=1),
                       bins=np.linspace(0, 1, 11), include_lowest=True)
pos = (df.assign(pos=(df.groupby("dialogue_id").cumcount() /
                      (df.groupby("dialogue_id")["turn_id"].transform("count") - 1).clip(lower=1)))
       )
pos["pos_bin"] = pd.cut(pos["pos"], bins=np.linspace(0, 1, 11), include_lowest=True)
track = ["rapport_building", "personal_story", "donation_procedure_information",
         "gratitude_and_appreciation", "minimization_framing", "persistent_repetition",
         "logical_appeal", "emotion_appeal"]
fig, ax = plt.subplots(figsize=(9, 5))
xs = np.arange(10) / 9
_seen = {}
for s in track:
    c = CATCOLOR[STRAT2CAT[s]]
    ls = "--" if _seen.get(STRAT2CAT[s]) else "-"
    _seen[STRAT2CAT[s]] = True
    y = pos.groupby("pos_bin", observed=False)["strategies"].apply(
        lambda col: np.mean([s in r for r in col]) * 100)
    ax.plot(xs, y.values, marker="o", ms=4, ls=ls, label=s, color=c)
ax.set(xlabel="normalised position in dialogue (0 = first turn, 1 = last)",
       ylabel="% of turns in bin", title="Selected strategies across dialogue progression")
ax.legend(fontsize=7, ncol=2)
save(fig, "09_strategy_by_position.png")

# 10. mean labels per turn along the corpus (global_index) --------
fig, ax = plt.subplots(figsize=(10, 4))
roll = df.set_index("global_index")["n_labels"].rolling(200, min_periods=50).mean()
ax.plot(roll.index, roll.values, color=PAL)
b = 0
for seg in SEG_ORDER if False else ["shimanto", "shovon", "unassigned", "shovon", "abhishek"]:
    pass
for x in [2000, 4000, 6000, 7000]:
    ax.axvline(x, color="0.6", ls="--", lw=1)
for x, lab in [(1000, "shimanto"), (3000, "shovon"), (5000, "unassigned"),
               (6500, "shovon"), (8800, "abhishek")]:
    ax.text(x, ax.get_ylim()[1]*0.95, lab, ha="center", fontsize=8, color="0.3")
ax.set(xlabel="global turn index", ylabel="mean n_labels (rolling 200)",
       title="Label density along the corpus - segment boundaries dashed")
save(fig, "10_label_density_along_corpus.png")

# 11. dialogue length + text length ------------------------------
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
tpd = df.groupby("dialogue_id").size()
axes[0].hist(tpd, bins=range(tpd.min(), tpd.max()+2), color=PAL, align="left")
axes[0].set(title=f"Persuader turns per dialogue (n={df['dialogue_id'].nunique()})",
            xlabel="annotated turns", ylabel="dialogues")
axes[1].hist(df["text_len"].clip(upper=60), bins=30, color="#55A868")
axes[1].set(title="Turn length (words, clipped at 60)", xlabel="words", ylabel="turns")
save(fig, "11_dialogue_and_text_length.png")

# 12. flags ------------------------------------------------------
fc = collections.Counter()
for row in df["flags"]:
    fc.update(row or ["<none>"])
fs = pd.Series(fc).sort_values()
fig, ax = plt.subplots(figsize=(7, 3.5))
bars = ax.barh(fs.index, fs.values, color="#8172B2")
ax.bar_label(bars, fmt="%d", fontsize=8)
ax.set(xlabel="turns", title="Flags")
save(fig, "12_flags.png")

# 13. rank-frequency (Zipf) of strategies -----------------------
ranked = sorted(sc.values(), reverse=True)
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.loglog(range(1, len(ranked)+1), ranked, marker="o", color=PAL)
ax.set(xlabel="rank", ylabel="turns (log)", title="Strategy rank-frequency (Zipf view)")
save(fig, "13_strategy_rank_frequency.png")

# 14. correlation of strategy indicators (phi) -----------------
wide = pd.DataFrame({s: df["strategies"].apply(lambda r: int(s in r)) for s in STRATS})
corr = wide.corr().fillna(0)
order_s = [s for c in CATS for s in TAX["categories"][c]["strategies"]]
corr = corr.loc[order_s, order_s]
fig, ax = plt.subplots(figsize=(13, 11))
sns.heatmap(corr, cmap="coolwarm", center=0, vmin=-.3, vmax=.3, ax=ax,
            square=True, cbar_kws={"label": "phi correlation"})
ax.set_title("Strategy co-label correlation (ordered by category)")
save(fig, "14_strategy_correlation.png")

print("\nEDA complete ->", EDA)
