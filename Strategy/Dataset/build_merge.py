"""
Merge the four phase-1 annotation segments into a single ordered dataset.

Canonical order == row order of persuader_turns.csv (10,600 persuader turns).
Segment -> annotator -> global rows (0-indexed):
    0000-1999  shimanto    annotation_first_2000_shimanto
    2000-3999  shovon      annotation_shovon  (turns 2001-4000)
    4000-5999  unassigned  annotation_turns_4001_6000  (model_id claude-opus-3.7-batch)
    6000-6999  shovon      annotation_shovon  (turns 6001-7000)
    7000-10599 abhishek    annotation_7001_10600_abhishek

Outputs (in this folder):
    multilabel_merged.jsonl        one record per turn, harmonised schema
    multilabel_merged.csv          flat, pipe-separated list columns
    multilabel_merged_wide.csv     10600 x (2 id + 41 has_* + 11 cat_*) binary matrix
"""
import csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # .../phase1
OUT  = Path(__file__).resolve().parent                 # .../phase1/merged_dataset
TAX  = json.loads((ROOT / "taxonomy_multilabel.json").read_text(encoding="utf-8"))

STRATS, STRAT2CAT = [], {}
for cat, cv in TAX["categories"].items():
    for s in cv["strategies"]:
        STRATS.append(s)
        STRAT2CAT[s] = cat
CATS = list(TAX["categories"].keys())

SEGMENTS = [
    ("shimanto",   "annotation_first_2000_shimanto/annotation_first_2000/claude_multilabel_first2000.jsonl", None),
    ("shovon",     "annotation_shovon/merged_multilabel_shovon.jsonl",                                       (0, 2000)),
    ("unassigned", "annotation_turns_4001_6000/merged_multilabel_turns_4001_6000.jsonl",                     None),
    ("shovon",     "annotation_shovon/merged_multilabel_shovon.jsonl",                                       (2000, 3000)),
    ("abhishek",   "annotation_7001_10600_abhishek/annotation_7001_10600/claude_multilabel_7001_10600.jsonl", None),
]

# ---- load canonical order --------------------------------------------------
order = list(csv.DictReader((ROOT / "persuader_turns.csv").open(encoding="utf-8")))
pos = {r["turn_id"]: i for i, r in enumerate(order)}
assert len(pos) == len(order) == 10600, (len(pos), len(order))

# ---- gather annotation records -------------------------------------------
recs = {}
for annot, rel, sl in SEGMENTS:
    lines = [json.loads(l) for l in (ROOT / rel).open(encoding="utf-8") if l.strip()]
    if sl:
        lines = lines[sl[0]:sl[1]]
    for r in lines:
        tid = r["turn_id"]
        if tid in recs:
            sys.exit(f"duplicate turn_id across segments: {tid}")
        r["annotator"] = annot
        recs[tid] = r

missing = set(pos) - set(recs)
extra   = set(recs) - set(pos)
if missing or extra:
    sys.exit(f"mismatch vs persuader_turns.csv  missing={len(missing)} extra={len(extra)}\n"
             f"  e.g. missing {list(missing)[:3]}  extra {list(extra)[:3]}")

# ---- emit in canonical order --------------------------------------------
merged = []
for gi, row in enumerate(order):
    r = recs[row["turn_id"]]
    strategies = list(r.get("strategies") or [])
    categories = list(r.get("categories") or [])
    # rebuild categories from strategies to guarantee consistency
    cat_from_strat = sorted({STRAT2CAT[s] for s in strategies if s in STRAT2CAT},
                            key=CATS.index)
    rec = {
        "global_index": gi,
        "turn_id": r["turn_id"],
        "dialogue_id": r["dialogue_id"],
        "turn_index": r.get("turn_index"),
        "conversation_id": row.get("conversation_id"),
        "persuader_turn_index": row.get("persuader_turn_index"),
        "n_turns_in_dialogue": row.get("n_turns_in_dialogue"),
        "annotator": r["annotator"],
        "strategies": strategies,
        "categories": cat_from_strat if cat_from_strat else categories,
        "n_labels": len(strategies),
        "flags": list(r.get("flags") or []),
        "note": r.get("note", "") or "",
        "text": r.get("text", "") or row.get("text", ""),
    }
    merged.append(rec)

# sanity: category mismatch report
mism = sum(1 for m in merged
           if sorted(m["categories"]) != sorted({STRAT2CAT[s] for s in m["strategies"] if s in STRAT2CAT}))
print(f"category rebuild adjusted rows: {mism}")

# ---- 1. JSONL -----------------------------------------------------------
with (OUT / "multilabel_merged.jsonl").open("w", encoding="utf-8", newline="\n") as f:
    for m in merged:
        f.write(json.dumps(m, ensure_ascii=False) + "\n")

# ---- 2. normal CSV (pipe-separated lists) ------------------------------
cols = ["global_index", "turn_id", "dialogue_id", "turn_index", "conversation_id",
        "persuader_turn_index", "n_turns_in_dialogue", "annotator",
        "strategies", "categories", "n_labels", "flags", "note", "text"]
with (OUT / "multilabel_merged.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(cols)
    for m in merged:
        w.writerow([
            m["global_index"], m["turn_id"], m["dialogue_id"], m["turn_index"],
            m["conversation_id"], m["persuader_turn_index"], m["n_turns_in_dialogue"],
            m["annotator"],
            "|".join(m["strategies"]), "|".join(m["categories"]),
            m["n_labels"], "|".join(m["flags"]), m["note"], m["text"],
        ])

# ---- 3. wide CSV (binary matrix) --------------------------------------
wide_cols = (["turn_id", "dialogue_id", "annotator"]
             + [f"has_{s}" for s in STRATS]
             + [f"cat_{c.replace(' ', '_')}" for c in CATS])
with (OUT / "multilabel_merged_wide.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(wide_cols)
    for m in merged:
        sset, cset = set(m["strategies"]), set(m["categories"])
        w.writerow([m["turn_id"], m["dialogue_id"], m["annotator"]]
                   + [1 if s in sset else 0 for s in STRATS]
                   + [1 if c in cset else 0 for c in CATS])

print(f"wrote {len(merged)} rows -> {OUT}")
print("  multilabel_merged.jsonl / .csv / _wide.csv")
