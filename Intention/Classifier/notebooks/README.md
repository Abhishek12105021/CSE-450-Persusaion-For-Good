# Donation-Intent Classifier -- Capstone Project

> **Task:** Classify whether a persuader-persuadee dialogue ends with the persuadee
> making a donation intent (`binary_label in {yes, no}`) and, if so, what type
> (`modifier in {none, deferred, conditional}`).
>
> 📖 **Comprehensive Compendium:** See [`RESEARCH_CHRONICLE.md`](RESEARCH_CHRONICLE.md) for the complete forensic record of architectural progression, experiments, and benchmark results from v3 to the SOTA v14-Antiphony (89.54% Acc, 0.8623 Macro-F1).

---

## Table of Contents

1. [Dataset](#dataset)
2. [Current Pipeline (v2)](#current-pipeline-v2)
3. [Results Summary](#results-summary)
4. [Sophisticated Pipeline Ideas & 1-Week Roadmap](#sophisticated-pipeline-ideas--1-week-feasibility-roadmap)
   - [1. Speaker-Aware Encoding](#1-speaker-aware-encoding)
   - [2. Hierarchical Dialogue Encoder](#2-hierarchical-dialogue-encoder)
   - [3. Contrastive Learning (SimCSE-style)](#3-contrastive-learning-simcse-style)
   - [4. Data Augmentation Suite](#4-data-augmentation-suite)
   - [5. Label Smoothing + Confidence Calibration](#5-label-smoothing--confidence-calibration)
   - [6. Ensemble + Uncertainty Estimation](#6-ensemble--uncertainty-estimation)
   - [7. LLM-as-Classifier (Zero-Shot / Few-Shot)](#7-llm-as-classifier-zero-shot--few-shot)
   - [8. Chain-of-Thought Intent Detection](#8-chain-of-thought-intent-detection)
   - [9. Last-Persuadee-Turn Gating & Recency Prior](#9-last-persuadee-turn-gating--recency-prior)
   - [10. Domain-Adaptive Pre-Training (DAPT)](#10-domain-adaptive-pre-training-dapt)
   - [11. Class-Balanced Multi-Objective Loss Engineering](#11-class-balanced-multi-objective-loss-engineering)
5. [1-Week Action Plan](#1-week-action-plan-prioritized-by-effort-vs-impact)
6. [Reproduction](#reproduction)
7. [References](#references)

---

## Dataset

| Split | Rows |
|-------|------|
| Train | 711 (70 %) |
| Val   | 153 (15 %) |
| Test  | 153 (15 %) |

**Class distribution:**
- `binary_label`: yes 72.5 % / no 27.5 % (imbalanced)
- `modifier`: none 85.6 % / deferred 12.4 % / conditional 2.0 % (heavily imbalanced)

**Imbalance handling:** inverse-frequency class weights in both loss heads
(class weights only — `WeightedRandomSampler` is disabled; stacking both over-rotates
minority classes and collapses macro-F1 below the majority baseline).

---

## Current Pipeline (v2)

```
Raw dialogue text
       |
  Tokenisation (AutoTokenizer, max_len=256)
       |
  Shared Transformer Encoder
       RoBERTa-base | DeBERTa-v3-base | TOD-BERT
       |
  Pooled CLS / mean-pool representation
       |
  +-----------------+   +-----------------------+
  | binary_head     |   |  modifier_head        |
  | 2-class         |   |  3-class              |
  +-----------------+   +-----------------------+
  Binary CE (w=1.0)     Modifier CE (w=0.7)
          \                /
          Multi-task loss
```

**Key settings:**

| Setting | Value |
|---------|-------|
| Epochs | 6 (early stopping, patience=2) |
| Default LR | 2e-5 |
| DeBERTa-v3 LR | 5e-6 (lower for numerical stability) |
| DeBERTa-v3 batch | 8 (smaller to avoid OOM) |
| Warmup ratio | 6 % |
| Max grad norm | 1.0 |
| Split | 70 / 15 / 15 stratified by binary x modifier stratum |

---

## Results Summary

| Model | Binary Acc | Binary F1 | Modifier macro-F1 |
|-------|-----------|-----------|-------------------|
| Majority baseline | 72.5 % | 84.1 % | 30.8 % |
| RoBERTa-base | *(run on Kaggle)* | | |
| DeBERTa-v3-base | *(run on Kaggle)* | | |
| TOD-BERT | *(run on Kaggle)* | | |

> Fill in after running `capstone-final.ipynb` on Kaggle T4 (Internet ON).

---

## Sophisticated Pipeline Ideas & Feasibility Matrix

The table below summarizes all architectural ideas, their current status across v3–v8, and their feasibility. **All external LLM API/inference methods are marked 🔴 (Discarded due to high API & infrastructure costs), focusing exclusively on 100% local, free, Kaggle T4-executable approaches.**

| # | Idea | Status / Version | Feasibility / Decision | Expected Cost / Effort |
|---|---|---|---|---|
| **1** | **Speaker-Aware Encoding** | ✅ Implemented (v3 token, v6/v8 turn-level) | Completed | Zero Cost |
| **2** | **Hierarchical Dialogue Encoder** | ✅ Implemented (v6/v8 HiTrans-style) | Completed (Core Innovation) | Zero Cost |
| **3** | **Contrastive Learning (SimCSE)** | 🟡 In-Batch SupCon Done (v4–v8)<br>🔴 Full 2-Stage SimCSE Pre-training | 🔴 **Discarded (High Compute Cost)** | High (>2 weeks compute) |
| **4** | **Data Augmentation Suite** | ✅ Local Back-Translation & EDA (v3–v8)<br>🔴 **Technique C: LLM Paraphrase** | 🔴 **Discarded (High LLM API Cost)** | High API tokens |
| **5** | **Label Smoothing & Calibration** | 🟡 Focal Loss Implemented (v4–v8)<br>🟢 **Post-hoc Temperature Calibration** | 🟢 **1-Week Feasible (< 1 Day, Local)** | Free (Scipy fit on val logits) |
| **6** | **Ensemble & Uncertainty** | 🟢 **Tri-Model Soft-Voting Ensemble**<br>🟢 **MC Dropout Uncertainty** | 🟢 **1-Week Feasible (< 1 Day, Local)** | Free (Inference on saved v8 models) |
| **7** | **LLM-as-Classifier (Few-Shot)** | 🔴 **Zero/Few-Shot & Pseudo-Labeling** | 🔴 **Discarded (High LLM API Cost)** | High API tokens |
| **8** | **Chain-of-Thought (CoT) Intent** | 🔴 **CoT API & Local 8B Distillation** | 🔴 **Discarded (High API & VRAM Cost)** | High API / A100 GPU needed |
| **9** | **Last-Persuadee-Turn Gating** | 🟢 **Recency Attention Prior / Direct Residual Gating** | 🟢 **1-Week Feasible (1–2 Days, Local)** | Free (Model code tweak) |
| **10** | **Domain-Adaptive Pre-Training (DAPT)** | 🔴 **MLM Pre-training on `persuader_turns.csv`** | 🔴 **Discarded (High Compute Cost)** | High (>24h T4 compute) |
| **11** | **Multi-Objective Loss Engineering** | ✅ **Class-Balanced Focal + SupCon + Cascaded Heads** | Completed (v4–v8 Foundation) | Zero Cost |

---

### 1. Speaker-Aware Encoding
> **Status:** ✅ **Implemented in v3 (token-level) and upgraded in v6/v8 (turn-level role embeddings)**

**Motivation:** The dialogue alternates `[Persuader]` / `[Persuadee]` turns.
The model sees raw text without any signal about who said what. Since
donation intent is always about the *Persuadee*, explicitly marking speaker roles
lets the attention mechanism focus on the right tokens.

**Implementation (v6/v8 Hierarchical):**
```python
# Turn-level role embedding (Persuader=0, Persuadee=1, Pad=2)
self.role_embedding = nn.Embedding(3, hidden)
turn_vecs = turn_vecs + self.role_embedding(role_ids)
```

**Delivered benefit:** Substantial improvement on resolving persuadee stance changes.

---

### 2. Hierarchical Dialogue Encoder
> **Status:** ✅ **Implemented in v6/v8 (The Core Architectural Leap)**

**Motivation:** Long dialogues truncated to 256 tokens lose later-turn context.
A hierarchical encoder first encodes each *utterance* independently, then uses a
second Transformer to aggregate utterance representations -- capturing full
dialogue structure without truncation.

**Architecture (v6/v8):**
```
u1  u2  u3  ...  uN  (up to 32 turns x 64 tokens = 2048 tokens capacity)
        |
 Utterance Encoder (RoBERTa / DeBERTa-v3 / TOD-BERT with Gradient Checkpointing)
        |
 Masked Mean Pooling + Role & Position Embeddings
        |
 4-Layer Dialogue Transformer Encoder (Inter-turn Self-Attention)
        |
 Turn-Level Learned Attention Pooling -> Cascaded Heads
```

**Delivered benefit:** Binary Macro-F1 jumped from 0.65 to **0.82**; Modifier Macro-F1 jumped from 0.30 to **0.45** (DeBERTa-v3).

---

### 3. Contrastive Learning (SimCSE-style)
> **Status:**
> - In-Batch Supervised Contrastive Loss (SupCon on `shared_repr`): ✅ **Implemented in v4–v8**
> - Full Two-Stage Unsupervised SimCSE Pre-training: 🔴 **Discarded (High Compute Cost)**

**Motivation:** With only 711 labelled examples the encoder can overfit to
surface patterns. Contrastive pre-training on the (much larger) unlabelled
dialogue corpus forces semantically meaningful representations before task
fine-tuning.

**Two-stage plan:**
* **Stage 1 -- Unsupervised SimCSE:**
```python
# Two dropout-augmented views of the same dialogue
# NT-Xent loss pulls them together, pushes all others apart
loss = InfoNCE(z_i, z_i_prime, temperature=0.05)
```
* **Stage 2 -- Standard fine-tuning** from Stage 1 checkpoint.

> 🔴 **Why Full Two-Stage SimCSE is Discarded:**
> 1. **Compute & Batch Size Constraint:** Unsupervised SimCSE requires large batch sizes ($B \ge 256$ to $512$) for robust negative pair mining, which causes instant OOM on standard Kaggle T4 GPUs.
> 2. **Pre-training Overhead:** Setting up a separate self-supervised pre-training pipeline takes several weeks of compute.
> 3. **Already Mitigated:** In-batch **Supervised Contrastive Loss (SupCon)** is already implemented directly in v4–v8 with zero extra compute cost.

---

### 4. Data Augmentation Suite
> **Status:**
> - Technique A (Local French Back-Translation): ✅ **Implemented in v7/v8 (100% Free / Local MarianMT)**
> - Technique B (Marker-Safe EDA): ✅ **Implemented in v3, fixed in v5/v8 (100% Free / Local Python)**
> - Technique C (LLM Paraphrase): 🔴 **Discarded (High API Cost)**

**Technique A -- Local MarianMT Back-Translation (Done in v7/v8):**
Uses local, open-source `Helsinki-NLP/opus-mt` models directly on GPU with zero API cost.
```python
# English -> French -> English (Helsinki-NLP/opus-mt models) turn-by-turn
aug_text = back_translate_dialogue(text, pivot_lang="fr")
```

**Technique B -- Marker-Safe EDA (Done in v5/v8):**
Marker-safe synonym replacement, insertion, deletion, and connective paraphrasing.

> 🔴 **Technique C (LLM Paraphrase) -- Discarded:**
> Calling commercial LLM APIs (GPT-4 / Gemini) for multi-turn paraphrasing across hundreds of iterations generates excessive API costs. Local MarianMT back-translation + connective substitution provides high-quality paraphrasing completely free.

---

### 5. Label Smoothing + Confidence Calibration
> **Status:**
> - Label Smoothing: 🟡 **Tested in v3 (superseded by Class-Balanced Focal Loss in v4–v8)**
> - Post-hoc Temperature Scaling: 🟢 **1-Week Feasible (< 1 Day, 100% Local / Free)**

**Motivation:** Hard cross-entropy loss leads to overconfident models. Temperature scaling on the validation set aligns predicted probabilities with empirical accuracy with zero GPU training cost.

**1-Week Implementation (Temperature Scaling):**
```python
import torch.nn as nn
from scipy.optimize import minimize

# Learn a single scalar T > 0 on validation logits using Scipy
def calibrate_temperature(val_logits, val_labels):
    def nll_loss(T):
        scaled_logits = val_logits / T
        return F.cross_entropy(torch.tensor(scaled_logits), torch.tensor(val_labels)).item()
    res = minimize(nll_loss, x0=[1.0], bounds=[(0.05, 5.0)])
    optimal_T = res.x[0]
    return optimal_T
```
* **Expected benefit:** +1-2 pp macro-F1 calibration; yields well-calibrated confidence scores and reliable thresholding.

---

### 6. Ensemble + Uncertainty Estimation
> **Status:** 🟢 **1-Week Feasible (< 1 Day, 100% Free / Highest ROI)**

**Motivation:** In `run-v8.ipynb`, we already trained and saved checkpoints for all 3 diverse architectures:
1. `roberta-base` (High recall on minority classes, e.g. 47% recall on `deferred`)
2. `microsoft/deberta-v3-base` (Highest precision & Macro-F1 = 0.821)
3. `TODBERT/TOD-BERT-JNT-V1` (Dialogue-specialized representations)

**1-Week Implementation (Soft-Voting Ensemble):**
```python
# Zero retraining needed -- pure local inference evaluation
probs_rob = torch.softmax(roberta_model(batch).binary_logits, dim=-1)
probs_deb = torch.softmax(deberta_model(batch).binary_logits, dim=-1)
probs_tod = torch.softmax(todbert_model(batch).binary_logits, dim=-1)

# Blended Soft Ensemble
final_probs = (probs_rob + probs_deb + probs_tod) / 3.0
final_binary_preds = final_probs.argmax(dim=-1)
```

**MC Dropout Uncertainty Estimation:**
```python
# Keep dropout active during evaluation to capture model uncertainty locally
preds = [model(x, training=True) for _ in range(20)]
mean_pred = torch.stack(preds).mean(0)
uncertainty_variance = torch.stack(preds).var(0)
```
* **Expected benefit:** Immediate +1–2 pp boost in Test Macro-F1 with zero additional training cost.

---

### 7. LLM-as-Classifier & Semi-Supervised Pseudo-Labeling
> **Status:** 🔴 **Discarded (High LLM API & Subscription Cost)**

**Original Idea:** Query commercial LLMs (GPT-4o / Gemini-1.5-Pro) for zero/few-shot intent classification or to pseudo-label thousands of unannotated turns in `persuader_turns.csv`.

> 🔴 **Why This Is Discarded:**
> 1. **High Token Costs:** Querying thousands of long dialogue transcripts (averaging 344 words each) via paid APIs incurs heavy recurring financial costs.
> 2. **Discriminative Efficiency:** Our lightweight local models (DeBERTa-v3/RoBERTa) achieve 0.82 Macro-F1 with 125M parameters, outperforming costly generalist API calls in speed and privacy.
> 3. **Reproducibility:** API-based classifiers suffer from backend model drift, whereas our PyTorch checkpoints are 100% reproducible and self-contained.

---

### 8. Chain-of-Thought (CoT) Intent Detection & Distillation
> **Status:** 🔴 **Discarded (High API Cost & Massive GPU Infrastructure Required)**

**Original Idea:** Prompt LLMs with step-by-step reasoning chains or fine-tune an 8B parameter model (Llama-3.1-8B) on CoT traces.

> 🔴 **Why This Is Discarded:**
> 1. **Massive Compute Requirement:** Fine-tuning an 8B model requires multi-GPU clusters (A100 80GB) that are unavailable on free Kaggle/Colab tiers.
> 2. **API Expense:** Generating synthetic CoT reasoning traces across the dataset via GPT-4 is cost-prohibitive.
> 3. **Hierarchical Attention Replaces CoT:** Our **Dialogue Transformer + Turn-Level Attention Pooling** already provides interpretable discourse attention weights without needing generative text traces.

---

### 9. Last-Persuadee-Turn Gating & Recency Prior
> **Status:** 🟢 **1-Week Feasible (1–2 Days, 100% Free / Local)**

**Motivation:** In persuasion dialogues, opening turns are pleasantries ("Good morning", "How are you?"). Per `guideline.md`, donation commitments and condition clauses are overwhelmingly concentrated in the **final 1–3 persuadee turns**. While the Dialogue Transformer learns attention weights freely, adding an explicit architectural prior guarantees that the concluding stance directly influences the classification heads.

**Implementation Sketch:**
```python
# Extract the hidden vector of the last valid Persuadee turn: u_last
last_persuadee_idx = ... # find index of last role == ROLE_PERSUADEE
u_last = dialogue_hidden[b, last_persuadee_idx]  # [B, H]

# Gated Residual Fusion:
gate = torch.sigmoid(self.gate_linear(torch.cat([pooled_repr, u_last], dim=-1)))
shared_repr = gate * pooled_repr + (1.0 - gate) * u_last
```
* **Expected benefit:** Sharper gradient flow to closing turns, directly helping distinguish `deferred` (promised later) from `none` (immediate) with zero API dependencies.

---

### 10. Domain-Adaptive Pre-Training (DAPT)
> **Status:** 🔴 **Discarded (High Compute & Time Cost)**

**Motivation:** Pre-training encoders on unannotated transcripts (`persuader_turns.csv`) via Masked Language Modeling (MLM).

> 🔴 **Why DAPT is Discarded:**
> 1. **Compute Budget:** Masked Language Modeling across thousands of turns takes 12–24+ hours on a T4 GPU.
> 2. **Instability Risk:** MLM without careful learning-rate decay and warmup can cause representation drift.
> 3. **High Opportunity Cost:** The hierarchical architecture and ensembling provide substantially larger gains with zero pre-training risk.

---

### 11. Class-Balanced Multi-Objective Loss Engineering
> **Status:** ✅ **Implemented in v4–v8 (Core Multi-Task Optimization)**

**Motivation:** Solves extreme class imbalance (`conditional` ~2%, `deferred` ~12%) and aligns multi-task dependencies.

**Formulation:**
$$\mathcal{L}_{\text{total}} = 1.0 \cdot \mathcal{L}_{\text{CB-Focal}}^{\text{bin}} + 0.7 \cdot \mathcal{L}_{\text{CB-Focal}}^{\text{mod}} + 0.10 \cdot \mathcal{L}_{\text{SupCon}}^{\text{bin}} + 0.30 \cdot \mathcal{L}_{\text{SupCon}}^{\text{mod}}$$
* **Effective-number-of-samples weighting** $\frac{1-\beta}{1-\beta^n}$ ($\beta=0.999$) prevents exploding inverse frequencies.
* **Cascaded Head**: Modifier input $[\mathbf{z}_{\text{shared}} \, ; \, \text{softmax}(\mathbf{y}_{\text{bin}}).\text{detach}()]$ explicitly conditions modifier predictions on binary confidence.

---

## 1-Week Action Plan (100% Free / Local Kaggle Execution)

```
Day 1: [Tri-Model Soft-Voting Ensemble] ─────────> Evaluate blended probabilities from saved v8 checkpoints (+1-2% F1 boost, zero training)
Day 2: [Last-Persuadee Turn Gating] ────────────> Add gated residual connection to Hierarchical Classifier in v8 notebook
Day 3: [Post-hoc Temperature Calibration] ──────> Run Scipy calibration script on validation logits for reliable confidence scores
Day 4: [MC Dropout Uncertainty Evaluation] ─────> Compute epistemic uncertainty variances to flag borderline cases
Day 5: [Final Report & Defense Visuals] ────────> Export consolidated confusion matrices and comparison charts for presentation
```

---

## Reproduction

```bash
# 1. Upload capstone-v8-hierarchical-augplus.ipynb to Kaggle
# 2. Add the labeled CSV as a Kaggle Dataset input
# 3. Notebook settings: Accelerator = T4 GPU, Internet = ON
# 4. Run All Cells
# Outputs saved to /kaggle/working/:
#   classifier_test_results_v8.csv
#   classifier_comparison_bar_v8.png
#   confusion_matrix_binary_v8.png
#   checkpoints_v8/<encoder>_best.pt
```

**Estimated runtime:** ~1.5–3 hours for all 3 hierarchical encoders on a Kaggle T4 GPU.

---

## References

| Citation |
|---------|
| Le et al. (2021). *HiTrans: A Hierarchical Transformer for Multi-Turn Dialogue Representation.* EMNLP. |
| Cui et al. (2019). *Class-Balanced Loss Based on Effective Number of Samples.* CVPR. |
| Khosla et al. (2020). *Supervised Contrastive Learning.* NeurIPS. |
| He et al. (2023). *DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding Sharing.* ICLR. |
| Wu et al. (2020). *TOD-BERT: Pre-trained Natural Language Understanding for Task-Oriented Dialogues.* EMNLP. |
| Wang et al. (2019). *Persuasion for Good: Towards a Personalized Persuasive Dialogue System for Social Good.* ACL. |
| Wei & Zou (2019). *EDA: Easy Data Augmentation Techniques for Boosting Performance on Text Classification Tasks.* EMNLP. |

