"""
Dataset Leakage & Diversity Audit
==================================
Measures whether a dialogue corpus can be solved by shortcuts instead of
language. Run this before any fine-tuning run.

The three metrics that matter for label leakage:

  * outcome-from-turn_count   -- can a model hit the label by counting turns?
  * outcome-from-last-intent  -- does the final intent tag give it away?
  * unique intent paths       -- how many distinct discourse routes exist?

A healthy synthetic split should sit near the human/LLM-authored seed
baseline on all three. Anything approaching 100% on the first two means the
evaluation is measuring the generator, not the model.

Usage:
    python audit_dataset.py [dataset.json ...]
"""

import sys
import os
import json
import re
import random
from collections import Counter, defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

SEED_MODELS = {"claude", "gemini", "gpt", "deepseek", "qwen-72b"}


def shell(text):
    """Strip digits so template reuse shows through price/number slots."""
    return re.sub(r"[\d,]+", "#", text)


def majority_accuracy(items, keyfn, labelfn):
    """Accuracy of always predicting the majority label within each key.

    In-sample: a key seen once memorizes its own label, so this is only
    meaningful for LOW-cardinality keys (turn_count, intent tags). For
    high-cardinality keys such as raw turn text, use holdout_accuracy --
    otherwise the score is 100% by construction and measures nothing.
    """
    groups = defaultdict(Counter)
    for x in items:
        groups[keyfn(x)][labelfn(x)] += 1
    correct = sum(c.most_common(1)[0][1] for c in groups.values())
    return 100.0 * correct / len(items) if items else 0.0


def holdout_accuracy(items, keyfn, labelfn, folds=5, seed=0):
    """Leave-fold-out majority vote: fit on 4/5, predict the held-out 1/5.

    Unseen keys fall back to the global majority, so a key that appears
    exactly once can no longer memorize itself. This is the honest way to
    ask 'does this surface feature generalize to new dialogues?'
    """
    if not items:
        return 0.0
    idx = list(range(len(items)))
    random.Random(seed).shuffle(idx)
    correct = 0
    for f in range(folds):
        test = {idx[i] for i in range(f, len(idx), folds)}
        train_groups = defaultdict(Counter)
        globalc = Counter()
        for i, x in enumerate(items):
            if i in test:
                continue
            train_groups[keyfn(x)][labelfn(x)] += 1
            globalc[labelfn(x)] += 1
        if not globalc:
            continue
        fallback = globalc.most_common(1)[0][0]
        for i in test:
            x = items[i]
            g = train_groups.get(keyfn(x))
            pred = g.most_common(1)[0][0] if g else fallback
            if pred == labelfn(x):
                correct += 1
    return 100.0 * correct / len(items)


def audit_group(name, dialogues):
    if not dialogues:
        return
    turns = [t for d in dialogues for t in d["turns"]]
    buyer = [t["text"] for t in turns if t["role"] == "Buyer"]
    merch = [t["text"] for t in turns if t["role"] == "Merchant"]
    label = lambda d: d["labels"]["outcome_category"]

    paths = [tuple(t["normalized_intent"] for t in d["turns"]) for d in dialogues]
    base = 100.0 * Counter(label(d) for d in dialogues).most_common(1)[0][1] / len(dialogues)
    tc_acc = holdout_accuracy(dialogues, lambda d: d["turn_count"], label)
    li_acc = holdout_accuracy(
        dialogues, lambda d: d["turns"][-1]["normalized_intent"], label)
    lt_acc = holdout_accuracy(
        dialogues, lambda d: shell(d["turns"][-1]["text"])[:60], label)

    has_oi = sum(1 for t in turns if "original_intent" in t)

    print(f"\n  {name}  ({len(dialogues)} dialogues, {len(turns)} turns)")
    print(f"    {'-'*62}")
    print(f"    BASELINE  majority-class only            {base:>6.1f}%")
    print(f"    LEAKAGE   outcome from turn_count alone   {tc_acc:>6.1f}%  (+{tc_acc-base:>5.1f})")
    print(f"    LEAKAGE   outcome from last intent alone  {li_acc:>6.1f}%  (+{li_acc-base:>5.1f})")
    print(f"    LEAKAGE   outcome from last-turn template {lt_acc:>6.1f}%  (+{lt_acc-base:>5.1f})")
    print(f"    DIVERSITY unique intent paths             {len(set(paths)):>5} / {len(paths)}")
    print(f"    DIVERSITY buyer text reuse                {len(buyer)/max(len(set(buyer)),1):>6.2f}x")
    print(f"    DIVERSITY merchant text reuse             {len(merch)/max(len(set(merch)),1):>6.2f}x")
    bs = {shell(t) for t in buyer}
    ms = {shell(t) for t in merch}
    print(f"    DIVERSITY buyer template shells           {len(bs):>5} for {len(buyer)} turns")
    print(f"    DIVERSITY merchant template shells        {len(ms):>5} for {len(merch)} turns")
    print(f"    SCHEMA    turns with original_intent      {has_oi:>5} / {len(turns)}")

    lens = Counter(d["turn_count"] for d in dialogues)
    print(f"    LENGTH    range {min(lens)}-{max(lens)} turns, {len(lens)} distinct values")

    # Length overlap: for each outcome, the span of turn_counts it occupies.
    by_out = defaultdict(list)
    for d in dialogues:
        by_out[label(d)].append(d["turn_count"])
    print(f"    LENGTH    per-outcome turn_count spans:")
    for o in sorted(by_out):
        v = by_out[o]
        print(f"                {o:<24} {min(v):>3}-{max(v):<3} (n={len(v)})")


def audit_file(path):
    with open(path, "r", encoding="utf-8") as f:
        corpus = json.load(f)
    print("\n" + "=" * 70)
    print(f"  {os.path.basename(path)}  --  {len(corpus)} dialogues")
    print("=" * 70)

    # The organic rewrite appends "-organic" to source_model, so compare on
    # the base tag. Without this, every rewritten seed dialogue falls into
    # the GENERATED bucket and both split baselines become meaningless.
    base = lambda d: (d.get("source_model") or "").replace("-organic", "")
    seed = [d for d in corpus if base(d) in SEED_MODELS]
    gen = [d for d in corpus if base(d) not in SEED_MODELS]

    audit_group("SEED (LLM-authored baseline)", seed)
    audit_group("GENERATED", gen)
    audit_group("FULL CORPUS", corpus)

    print(f"\n  Archetype spread (generated): "
          f"{len(Counter(d.get('archetype') for d in gen))} distinct")
    print(f"  Outcome mix (full): {dict(Counter(d['labels']['outcome_category'] for d in corpus))}")


if __name__ == "__main__":
    files = sys.argv[1:] or [os.path.join(SCRIPT_DIR, "extended_dataset.json")]
    for p in files:
        audit_file(p)
    print()
