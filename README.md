# Antiphony: Dual-Perspective Modeling of Persuasion and Commitment in Asymmetric Dialogue

[![Course](https://img.shields.io/badge/BUET%20CSE-CSE%20450%20Capstone-blue.svg)](https://cse.buet.ac.bd/)
[![Institution](https://img.shields.io/badge/Institution-BUET-8A1538.svg)](https://www.buet.ac.bd/)
[![Final Report](https://img.shields.io/badge/Report-PDF%20Available-success.svg)](Final-Report/Report_G10.pdf)
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11-3776AB.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-EE4C2C.svg)](https://pytorch.org/)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-FFD21E.svg)](https://huggingface.co/)
[![Live App: Persuasion](https://img.shields.io/badge/Demo-Persuasion%20App-00C7B7.svg)](https://intentionalysis-persuasion.vercel.app)
[![Live App: Buyer--Seller](https://img.shields.io/badge/Demo-Buyer--Seller%20App-7928CA.svg)](https://intentionalysis-buyer-seller.vercel.app)

> **CSE 450 Capstone Project (Session 2024–2025)**  
> **Department of Computer Science and Engineering**  
> **Bangladesh University of Engineering and Technology (BUET)**  
> **Supervised by:** **Dr. Md. Shariful Islam Bhuyan**, Associate Professor, Department of CSE, BUET  
> **Team:** Group 10 (Arnob Biswas, Nawriz Ahmed Turjo, Abhishek Roy, Monjur Hossain Khan, Shams Hossain Simanto)

---

## 📑 Quick Links & Deliverables

| Deliverable | Location | Description |
| :--- | :--- | :--- |
| 📄 **Updated Final Report** | [`Final-Report/Report_G10.pdf`](Final-Report/Report_G10.pdf) | Complete, 60+ page compiled capstone final report with all chapters, diagrams, and proofs |
| 🛠️ **Report LaTeX Sources** | [`Final-Report/`](Final-Report/) | Fully reproducible LaTeX source package (`template.tex`, `cse-capstone.sty`, `chapters/`, `figures/`) |
| 📊 **Presentation Slides** | [`Presentation/final.pdf`](Presentation/final.pdf) · [`.pptx`](Presentation/Report_presentation_deck_setup.pptx) | Final defense presentation deck |
| 🖼️ **Academic Poster** | [`Poster/Group10_Antiphony.pdf`](Poster/Group10_Antiphony.pdf) | Comprehensive capstone project poster and architecture schematics |
| 📰 **Project Leaflet** | [`Leaflet/leaflet-antiphony.pdf`](Leaflet/leaflet-antiphony.pdf) | Condensed 2-page project summary and architectural handout |
| 🌐 **Live Demo (Charity Persuasion)** | [intentionalysis-persuasion.vercel.app](https://intentionalysis-persuasion.vercel.app) | Real-time persuasion workspace scoring donor commitments live |
| 🌐 **Live Demo (Commerce Negotiation)** | [intentionalysis-buyer-seller.vercel.app](https://intentionalysis-buyer-seller.vercel.app) | Real-time negotiation workspace scoring buyer commitment trajectories |

---

## 📖 Table of Contents

1. [Executive Summary & Motivation](#-executive-summary--motivation)
2. [Key Contributions & Findings](#-key-contributions--findings)
3. [System Architecture](#-system-architecture)
4. [Benchmark Performance & SOTA Results](#-benchmark-performance--sota-results)
5. [Repository Structure & File Organization](#-repository-structure--file-organization)
6. [Environment Setup & Installation](#-environment-setup--installation)
7. [Step-by-Step Reproduction Guide](#-step-by-step-reproduction-guide)
   - [Track 1: Conversational Intention Classification](#track-1-conversational-intention-classification)
   - [Track 2: Rhetorical Strategy Attribution](#track-2-rhetorical-strategy-attribution)
   - [Track 3: Cross-Domain Negotiation & Diagnostic Ablation](#track-3-cross-domain-negotiation--diagnostic-ablation)
   - [Track 4: Compiling the Final Report from Source](#track-4-compiling-the-final-report-from-source)
8. [Demonstration Applications (Havn Platform)](#-demonstration-applications-havn-platform)
9. [Team Members & Contact](#-team-members--contact)
10. [Citation](#-citation)

---

## 🎯 Executive Summary & Motivation

Many real-world conversations are asymmetric attempts at persuasion: a fundraiser urging a donor to contribute, or an online merchant negotiating terms with a buyer over chat. In these dialogues, one party (the **Persuader**) actively deploys rhetorical moves and counter-offers, while the other party (the **Persuadee / Decider**) evaluates them and reaches a terminal stance.

Prior dialogue classification systems suffer from three major design flaws:
1. **Symmetric Flattening:** Treating multi-turn dialogues as monolithic text sequences, discarding speaker role boundaries, and running into quadratic self-attention memory limits that truncate conversations (losing >50% of dialogue history).
2. **Ground-Truth Divergence:** Benchmarks such as *Persuasion for Good* (P4G) rely on self-reported numeric donation fields that frequently contradict explicit statements in the chat transcripts (e.g., agreeing to donate \$10 while logged as \$0).
3. **Superficial Recency Bias:** Flat classifiers exploit isolated lexical tokens in closing turns rather than tracking the non-monotonic progression of commitment over time.

**Antiphony** resolves these limitations through:
- A **Dual-Perspective Architecture** that disentangles dialogues into role-pure streams and applies directional cross-attention ($\text{Decider} \to \text{Persuader}$).
- A **Three-Pass Ground-Truth Curation Protocol** providing verified, hedge-free intention labels.
- An **11-Category, 41-Strategy Hierarchical Taxonomy** covering 10,600 turns, modeled via a 19-member ensemble with calibrated power-mean blending.
- A **700-Dialogue E-Commerce Benchmark** containing adversarial stance reversals and counterfactual ablation operators, demonstrating a $+0.0384$ sufficiency gap lift that proves authentic trajectory tracking.

---

## 🔬 Key Contributions & Findings

| Area | Challenge | Antiphony Solution | Outcome |
| :--- | :--- | :--- | :--- |
| **Ground Truth** | Tabular donation records in P4G disagree with actual text statements. | 3-pass human annotation protocol enforcing terminal, unconditional commitment. | Verified benchmark: **694 yes / 323 no** (strict third pass) and **738 yes / 279 no** (second pass). |
| **Intention Modeling** | Flat transformers truncate turns or skew toward majority classes. | Role-pure stream separation, directional cross-attention ($\mathbf{Q}_{\mathcal{D}} \to \mathbf{K}_{\mathcal{P}}, \mathbf{V}_{\mathcal{P}}$), trajectory GRU. | **$0.8623$ Macro-F1** (Second-Pass, DeBERTa) and **$0.8446$ Macro-F1** (Strict Third-Pass, RoBERTa). |
| **Rhetorical Strategies** | Extreme long-tail imbalance on 41 fine strategies (down to 2 examples). | Multi-task category-first formulation (11 categories primary, 41 strategies auxiliary) under Asymmetric Loss. | **$0.7062$ Micro-F1 / $0.5642$ Macro-F1**, achieving **~89.4%** of the empirical human inter-annotator consensus ceiling (~0.79). |
| **Ensemble Blending** | Combining 19 heterogeneous members (transformers, few-shot, TF-IDF). | Evaluated machine-learned XGBoost stacker vs. Calibrated Power-Mean Blend ($q=+2.0$). | Power-mean blend achieves **$0.5716$ Val Macro-F1**, outperforming tuned XGBoost stacking ($0.5508$). |
| **Domain Transfer** | Dialogues overdetermined by terminal agreement cues. | 700 synthetic buyer--seller chats with 200 adversarial reversals and diagnostic input-ablation harness. | Sufficiency gap widens from $+0.0001$ (canonical) to **$+0.0384$** (adversarial reversals), proving trajectory dependency. |
| **Tokenizer Guard** | Standard right-truncation silently discards conversational decision points. | Enforced **left-truncation invariant** (`truncation_side='left'`). | Prevented an artificial $+0.1600$ diagnostic collapse under last-turn removal. |

---

## 🏗️ System Architecture

### 1. AntiphonyClassifier (Intention & Commitment Subsystem)
```
Input Dialogue D (up to 32 turns x 64 tokens = 2,048 token capacity)
               │
               ▼
   [Batched Encoder (DeBERTa-v3 / RoBERTa)] ──> Utterance Vectors U ∈ R^{B x U x d}
               │
      ┌────────┴────────┐
      ▼                 ▼
Persuader Stream   Decider Stream      (Role Disentanglement: R = 20 turns each)
   H^(P)             H^(D)
      │                 │
[Transformer_P]   [Transformer_D]
   H~^(P)            H~^(D)
      │                 │
      └───► [ Directional Cross-Attention ] ◄───┘
            Query = H~^(D), Key/Value = H~^(P)
            Decider attends to Persuader tactics
                        │
                        ▼
               Residual LayerNorm
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
   [Commitment-Trajectory GRU]   [Learned Attention Pooling]
       h_t = GRU(x_t, h_{t-1})          p = sum_t (α_t * x_t)
    (Read at true final decider)
             │                     │
             └──────────┬──────────┘
                        ▼
            Fused Representation z = [h_T ; p] ∈ R^{2d}
                        │
                        ▼
                 [2-Layer MLP Head]
                        │
                        ▼
       Binary Commitment Logits (yes / no)
   Loss: Class-Balanced Focal Loss + Supervised Contrastive Loss
```

### 2. Multi-Task Rhetorical Strategy Framework
- **Primary Objective:** 11 Communicative Categories (Relational, Information, Emotional, Social, Reciprocity, Framing, Credibility, Rational, Threat, Consistency, Urgency).
- **Auxiliary Regularizer:** 41 Fine-grained Strategies nested deterministically under categories.
- **Loss Function:** Asymmetric Loss (ASL) with hard probability margin shifting ($m=0.05$) and asymmetric focusing ($\gamma_+=0, \gamma_-=4$).
- **Decision Layer:** 19-member candidate pool combined via Platt-calibrated power-mean blend ($q=+2.0$).

---

## 📊 Benchmark Performance & SOTA Results

### Track 1: Conversational Intention Classification on P4G

#### Third-Pass Strict Unconditional Benchmark (694 Yes / 323 No, Held-Out Test $n=153$)
| Architecture | Encoder Backbone | Decision Threshold | Test Accuracy | Test Binary Macro-F1 | `No` F1 | `Yes` F1 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| *Majority Baseline* | *None* | 0.50 | 68.0% | 0.4047 | 0.0000 | 0.8095 |
| Decoupled Single-Stream | RoBERTa-base | Default (0.50) | 86.9% | 0.8359 | 0.7778 | 0.9082 |
| Decoupled Single-Stream | RoBERTa-base | Tuned (0.55) | 86.3% | 0.8290 | 0.7692 | 0.9038 |
| Decoupled Single-Stream | TOD-BERT | Tuned (0.60) | 84.3% | 0.8235 | 0.7600 | 0.8870 |
| Decoupled Single-Stream | DeBERTa-v3-base | Tuned (0.35) | 83.7% | 0.8134 | 0.7447 | 0.8821 |
| **Dual-Stream Antiphony (Ours)** | **RoBERTa-base** | **Tuned (0.70)** | **86.9%** | **0.8446** | **0.7826** | **0.9065** |
| Dual-Stream Antiphony (Ours) | RoBERTa-base | Default (0.50) | 86.3% | 0.8358 | 0.7660 | 0.9057 |
| Dual-Stream Antiphony (Ours) | TOD-BERT | Tuned (0.85) | 86.3% | 0.8378 | 0.7742 | 0.9014 |
| Dual-Stream Antiphony (Ours) | DeBERTa-v3-base | Tuned (0.90) | 84.3% | 0.8217 | 0.7600 | 0.8835 |

#### Second-Pass Benchmark (Modifier Dropped, 738 Yes / 279 No, Held-Out Test $n=153$)
| Architecture | Encoder Backbone | Threshold | Test Accuracy | Test Binary Macro-F1 |
| :--- | :--- | :---: | :---: | :---: |
| *Majority Baseline* | *None* | 0.50 | 72.5% | 0.4205 |
| Decoupled Single-Stream | RoBERTa-base | Tuned (0.70) | 86.9% | 0.8250 |
| **Dual-Stream Antiphony (Ours)** | **DeBERTa-v3-base** | **Default (0.50)** | **89.5%** | **0.8623** [SOTA] |
| Dual-Stream Antiphony (Ours) | DeBERTa-v3-base | Tuned (0.20) | 89.5% | 0.8600 |
| Dual-Stream Antiphony (Ours) | RoBERTa-base | Tuned (0.90) | 88.9% | 0.8595 |
| Dual-Stream Antiphony (Ours) | TOD-BERT | Tuned (0.45) | 87.6% | 0.8379 |

---

### Track 2: Rhetorical Strategy & Category Modeling (10,600 Turns)

| Modeling Stage | Target Formulation | Finished Encoders | Test Macro-F1 | Test Micro-F1 | Human Ceiling Proximity |
| :--- | :--- | :---: | :---: | :---: | :---: |
| 1. Strategy-Only Baseline | 39 fine strategies | 7 of 7 | 0.3680 | 0.5890 | 74.6% |
| 2. Category Initial Attempt | 11 categories (augmented) | 4 of 7 | 0.5555 | 0.6603 | 83.6% |
| 3. Category Clean Rerun | 11 categories (no aug) | 7 of 7 | 0.5539 | 0.6696 | 84.8% |
| 4. Multi-Task Candidate Pool | 11 cat (prim) / 41 strat (aux) | 19-member pool | 0.5593 | 0.6918 | 87.6% |
| **5. Power-Mean Ensemble ($q=+2.0$)** | **11 cat (prim) / 41 strat (aux)** | **19-member pool** | **0.5597** | **0.6949** | **88.0%** |
| **Micro-Optimal Operating Point** | **Bagged 19-Member Pool** | **19-member pool** | **0.5642** | **0.7062** | **89.4%** |

*Note on Human Ceiling:* Pairwise cross-annotator agreement on near-duplicate utterances yields an empirical ceiling of **$\approx 0.79$ Micro-F1**. Our shipped ensemble at $0.7062$ achieves nearly **90%** of human consensus.

---

### Track 3: Cross-Domain Negotiation Transfer & Adversarial Ablations

#### Augmented Negotiation Benchmark ($N=700$, Test $n=105$)
| Model Configuration | Backbone | Accuracy | Binary F1 | Macro-F1 | $\Delta$ over Baseline |
| :--- | :--- | :---: | :---: | :---: | :---: |
| Majority Baseline | *None* | 52.38% | 0.0000 | 0.3438 | 0.0000 |
| Last-Turn Localized Control | RoBERTa-base | 92.38% | 0.9200 | 0.9235 | +0.5797 |
| AntiphonyClassifier | RoBERTa-base | 95.24% | 0.9524 | 0.9524 | +0.6086 |
| **AntiphonyClassifier (Ours)** | **DeBERTa-v3-base** | **96.19%** | **0.9608** | **0.9619** | **+0.6181** |
| AntiphonyClassifier (Ours) | TOD-BERT | 96.19% | 0.9615 | 0.9619 | +0.6182 |

#### Widening of the Sufficiency Gap ($\Delta_{\text{suff}}$)
| Metric / Layer | Canonical Corpus ($N=500$) | Adversarial Reversal Corpus ($N=700$) | Trajectory Interpretation |
| :--- | :---: | :---: | :---: |
| Full Antiphony Model | 0.9733 | 0.9619 | Maintains robust trajectory modeling |
| Last-Turn Localized Control | 0.9732 | 0.9235 | Drops by $-0.0497$ under stance shifts |
| **Sufficiency Gap ($\Delta_{\text{suff}}$)** | **+0.0001 (+0.01%)** | **+0.0384 (+3.84%)** | **Proves full trajectory dependency** |

---

## 📂 Repository Structure & File Organization

```text
CSE 450 - Persuasion For Good/
│
├── Final-Report/                               # Capstone Final Report Package (Updated)
│   ├── Report_G10.pdf                          # Compiled Final Report (60+ pages) [SUPERVISOR DELIVERABLE]
│   ├── template.tex                            # LaTeX master document
│   ├── cse-capstone.sty                        # Official BUET CSE capstone stylesheet
│   ├── references.bib                          # BibTeX literature citations
│   ├── frontmatter/                            # Titlepage, declaration, acknowledgement, abstract
│   ├── chapters/                               # Chapters 1 through 7 (Problem, Research, Requirements,
│   │                                           #   Design, Evaluation, Management & Impact, Conclusion)
│   └── figures/                                # Architecture TikZ sources and high-res vector figures
│
├── Intention/                                  # Track 1: Conversational Intention & Commitment
│   ├── Classifier/
│   │   ├── notebooks on_updated_dataset/       # STRICT THIRD-PASS RUNS (694 yes / 323 no)
│   │   │   ├── ultimate-capstone-final-v14.ipynb # SOTA AntiphonyClassifier (RoBERTa, DeBERTa, TOD-BERT)
│   │   │   └── ultimate-capstone-final-v13.ipynb # Decoupled Single-Stream Baseline
│   │   ├── notebooks/
│   │   │   └── improvement-nb/                 # SECOND-PASS RUNS (738 yes / 279 no)
│   │   │       ├── capstone-v14-antiphony.ipynb # Second-Pass Antiphony SOTA (DeBERTa 0.8623)
│   │   │       ├── capstone-v13-solo.ipynb      # Decoupled Baseline
│   │   │       └── capstone-v10-coda.ipynb      # Last-Persuadee-Turn Gated Model
│   │   └── final-notebooks/                    # Architectural Evolution (M1 through M8)
│   │       ├── v1 - base.ipynb                 # M1 Flat 256-token Baseline
│   │       ├── v2 - speaker-aware-encoding.ipynb # M2 Role Embeddings
│   │       ├── v4 - data_aug+left_trunc.ipynb  # M4 CB-Focal + SupCon
│   │       └── v6 - hierarchical.ipynb         # M6 Hierarchical Transformer (HiTrans)
│   ├── Dataset/                                # First/Second Pass Annotations (738/279)
│   │   ├── Manual_Label.csv                    # Ground-truth labels with original modifiers
│   │   └── annotation_guidelines.md            # Pass 1 & 2 protocol documentation
│   └── Dataset_updated/                        # Strict Third-Pass Annotations (694/323)
│       ├── Manual_Label.csv                    # Final strict binary ground truth
│       ├── flip_recheck_report.md              # Audit report for all 81 remapped boundary cases
│       └── annotation_guidelines.md            # Strict third-pass protocol documentation
│
├── Strategy/                                   # Track 2: Turn-Level Persuasion Strategy Attribution
│   ├── Dataset/
│   │   ├── multilabel_merged.jsonl             # Primary dataset: 10,600 annotated Persuader turns
│   │   ├── multilabel_merged.csv               # Flat tabular view
│   │   ├── multilabel_merged_wide.csv          # 10,600 x 56 binary matrix (41 strategies + 11 categories)
│   │   ├── taxonomy_multilabel.json            # 2-tier hierarchical taxonomy definitions
│   │   ├── build_merge.py                      # Deterministic merge pipeline from raw annotator chunks
│   │   ├── build_eda.py                        # Full EDA reproduction script (generates all 14 figures)
│   │   └── eda/                                # 14 publication figures and statistical tables
│   ├── Annotation/                             # Annotation Protocols & Prompts
│   │   ├── pipeline.py                         # 5-turn causal contextual batching script
│   │   ├── prompt.md                           # Claude 5 Sonnet few-shot calibration prompt
│   │   ├── TAXONOMY_CHEATSHEET.md              # 4-tier decision protocol cheatsheet
│   │   └── ANNOTATION_PROCESS.md               # Audit trail of human checkpoints
│   └── Notebooks/
│       └── Final/
│           ├── multistrat-capstone_v17.ipynb   # 19-member Multi-Task Candidate Pool under ASL
│           └── multistrat-capstone_v18.ipynb   # Calibrated Power-Mean Blending & XGBoost Stacking
│
├── Generic/                                    # Track 3: Cross-Domain Negotiation & Diagnostic Ablation
│   ├── Dataset/
│   │   ├── generic_dataset.json                # Canonical benchmark (500 dialogues)
│   │   ├── build_advanced_dialogues.py         # DST-constrained dialogue synthesis script
│   │   ├── paraphase_pipeline.py               # Gemini organic paraphrasing with linguistic jitter
│   │   └── REVERSAL_DATASET_GUIDE.md           # Generation protocol for 200 adversarial reversals
│   ├── Final/
│   │   ├── ArmA/                               # Canonical N=500 diagnostic ablations (LTR, LTR+M, FHO)
│   │   │   ├── generic-ablation-lefttrunc.ipynb # Diagnostic harness enforcing left-truncation invariant
│   │   │   └── final.json                      # Audited canonical dataset
│   │   ├── ArmB/                               # Reversal N=200 subset
│   │   │   ├── gen-abl-b-strict.ipynb          # Stance-shift diagnostic ablation (LTR, PRO, FHO)
│   │   │   └── reversal_dataset_v3.json        # 200 verified reversal dialogues
│   │   └── ArmC/                               # Combined Augmented N=700 benchmark
│   │       ├── gen-abl-c-strict.ipynb          # Full ablation harness on augmented dataset
│   │       └── final_plus_reversal_v3.json     # Frozen 700-dialogue benchmark
│   └── ran-nb-reversal/
│       └── generic-antiphony-reversal.ipynb    # Antiphony Trajectory Evaluation on reversals
│
├── Leaflet/                                    # Project Summary Leaflet
│   └── leaflet-antiphony.pdf                   # 2-page publication summary handout
│
├── Poster/                                     # Academic Defense Poster
│   ├── Group10_Antiphony.pdf                   # Complete presentation poster
│   └── architecture/                           # High-res modular vector sub-diagrams
│
├── Presentation/                               # Defense Presentation Slides
│   ├── final.pdf                               # Slide deck (PDF format)
│   └── Report_presentation_deck_setup.pptx     # Slide deck (PowerPoint format)
│
├── Update-Report/                              # Mid-term progress archive
│   └── Pathao_Group_10.pdf                     # Mid-term report deliverable
│
├── .gitignore                                  # Git tracking configuration (LaTeX temp files excluded)
├── requirements.txt                            # Verified Python package dependencies
└── README.md                                   # Master repository documentation (This file)
```

---

## ⚙️ Environment Setup & Installation

### Prerequisites
- **Operating System:** Linux, macOS, or Windows 10/11
- **Python Version:** Python 3.10 or 3.11
- **GPU Hardware:** NVIDIA GPU with $\ge 8$\,GB VRAM (e.g., RTX 3070/4080, Tesla T4, V100, A100). Micro-batch slicing ($B=2$) and gradient checkpointing are built into notebooks to fit comfortably within 16\,GB VRAM (e.g., Kaggle / Colab free tiers).

### 1. Clone the Repository
```bash
git clone https://github.com/Abhishek12105021/CSE-450-Persusaion-For-Good.git
cd CSE-450-Persusaion-For-Good
```

### 2. Create and Activate a Virtual Environment
```bash
# Using conda (recommended)
conda create -n antiphony python=3.10 -y
conda activate antiphony

# Or using venv
python -m venv venv
# On Linux/macOS:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

### 3. Install Package Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Deterministic Reproducibility
All modeling scripts and notebooks invoke a unified random seeding routine:
```python
import random, os, numpy as np, torch

def seed_everything(seed=42):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True

seed_everything(42)
```

---

## 🚀 Step-by-Step Reproduction Guide

### Track 1: Conversational Intention Classification

#### Step 1.1: Shipped SOTA Model on Strict Third-Pass Dataset (694 Yes / 323 No)
1. Open the primary production notebook:
   ```bash
   jupyter notebook "Intention/Classifier/notebooks on_updated_dataset/ultimate-capstone-final-v14.ipynb"
   ```
2. Verify that the input data points to:
   - Dialogue Transcripts: `Intention/Dataset_updated/donation_intetion_manual_label_dataset.csv`
   - Strict Ground Truth: `Intention/Dataset_updated/Manual_Label.csv`
3. Execute all cells. The notebook will:
   - Partition dialogues into stratified 70/15/15 splits ($n=711$ train, $n=153$ val, $n=153$ test) using `random_state=42`.
   - Train `AntiphonyClassifier` across backbones (`roberta-base`, `microsoft/deberta-v3-base`, `jinserk/tod-bert-jnl-base`).
   - Run directional cross-attention and commitment-trajectory GRU readouts at true final decider turns.
   - Sweep threshold $\theta \in [0.10, 0.90]$ on validation set and evaluate out-of-fold on the test set.
   - **Expected Output:** Peak test **Macro-F1 of $0.8446$** (RoBERTa tuned $\theta=0.70$) and test Accuracy of **$86.9\%$**.

#### Step 1.2: Decoupled Single-Stream Baseline Comparison
1. Open:
   ```bash
   jupyter notebook "Intention/Classifier/notebooks on_updated_dataset/ultimate-capstone-final-v13.ipynb"
   ```
2. Run all cells to evaluate the flat hierarchical single-stream model without cross-attention.
3. **Expected Output:** Peak test Macro-F1 of **$0.8290$** (RoBERTa tuned) / **$0.8359$** (default), demonstrating the positive margin achieved by Antiphony ($+0.0156$).

#### Step 1.3: Second-Pass Dataset Reproduction (738 Yes / 279 No)
1. Open:
   ```bash
   jupyter notebook "Intention/Classifier/notebooks/improvement-nb/capstone-v14-antiphony.ipynb"
   ```
2. Execute all cells on `Intention/Dataset/Manual_Label.csv`.
3. **Expected Output:** Peak test **Macro-F1 of $0.8623$** (DeBERTa-v3-base, default $\theta=0.50$) and test Accuracy of **$89.5\%$**.

---

### Track 2: Rhetorical Strategy Attribution

#### Step 2.1: Recompile Merged Dataset & Run Exploratory Data Analysis (EDA)
1. Navigate to the strategy dataset directory:
   ```bash
   cd Strategy/Dataset
   ```
2. Run the deterministic dataset merger:
   ```bash
   python build_merge.py
   ```
   *Verifies taxonomy invariants, recomputes categories from strategies, and outputs `multilabel_merged.jsonl`, `multilabel_merged.csv`, and `multilabel_merged_wide.csv` (10,600 turns, 0 violations).*
3. Regenerate all 14 publication EDA figures:
   ```bash
   python build_eda.py
   ```
   *Generates plots in `Strategy/Dataset/eda/` (label density, co-occurrence matrices, positional trajectory, and rater granularity shifts).*
4. Return to root:
   ```bash
   cd ../..
   ```

#### Step 2.2: Multi-Task Candidate Pool Training (v17)
1. Open:
   ```bash
   jupyter notebook "Strategy/Notebooks/Final/multistrat-capstone_v17.ipynb"
   ```
2. Execute to train the 19-member candidate pool:
   - 7 fine-tuned transformers (RoBERTa, ELECTRA) under Asymmetric Loss ($\lambda_{\text{aux}}=0.20$).
   - 8 few-shot centroid classifiers.
   - 2 TF-IDF n-gram baselines + 2 zero-shot anchor matchers.
3. **Expected Output:** Multi-task candidate pool test **Micro-F1 of $0.6918$** / **Macro-F1 of $0.5593$**.

#### Step 2.3: Power-Mean Decision Blending & XGBoost Stacker Search (v18)
1. Open:
   ```bash
   jupyter notebook "Strategy/Notebooks/Final/multistrat-capstone_v18.ipynb"
   ```
2. Execute to run the decision combiner comparison:
   - Evaluates 72-configuration XGBoost stacking grid search (achieving tuned val Macro-F1 of $0.5508$).
   - Evaluates Platt-calibrated power-mean blend ($q=+2.0$, achieving tuned val Macro-F1 of $0.5716$).
3. **Expected Output:** Power-Mean Ensemble test **Micro-F1 of $0.6949$** / **Macro-F1 of $0.5597$** (Micro-optimal decode: **Micro-F1 $0.7062$** / **Macro-F1 $0.5642$**).

---

### Track 3: Cross-Domain Negotiation & Diagnostic Ablation

#### Step 3.1: Canonical Benchmark Input Ablation (Arm A, $N=500$)
1. Open:
   ```bash
   jupyter notebook "Generic/Final/ArmA/generic-ablation-lefttrunc.ipynb"
   ```
2. Run all cells to verify the **left-truncation invariant** (`truncation_side='left'`) across four ablation operators:
   - Full sequence: $0.9733$ Macro-F1.
   - Last-Turn-Removed ($\text{Ablation}_{\text{LTR}}$): $0.9331$ Macro-F1.
   - Last-Turn & Merchant Courtesy Removed ($\text{Ablation}_{\text{LTR+M}}$): $0.9331$ Macro-F1.
   - First-Half-Only ($\text{Ablation}_{\text{FHO}}$): $0.7707$ Macro-F1.

#### Step 3.2: Adversarial Reversal Stance Diagnostics (Arm B, $N=200$)
1. Open:
   ```bash
   jupyter notebook "Generic/Final/ArmB/gen-abl-b-strict.ipynb"
   ```
2. Run all cells on `Generic/Final/ArmB/reversal_dataset_v3.json`.
3. Verifies zero flip-error rate ($0/20$ errors) across both positive ($\text{resistance} \to \text{agreement}$) and negative ($\text{commit} \to \text{rejection}$) reversals.

#### Step 3.3: Augmented Reversal Transfer Benchmark (Arm C, $N=700$)
1. Open:
   ```bash
   jupyter notebook "Generic/Final/ArmC/gen-abl-c-strict.ipynb"
   ```
2. Run all cells on `Generic/Final/ArmC/final_plus_reversal_v3.json`.
3. Open `Generic/ran-nb-reversal/generic-antiphony-reversal.ipynb` to evaluate Antiphony trajectory tracking.
4. **Expected Output:**
   - Full Antiphony Model: **$0.9619$ Macro-F1** / **$96.19\%$ Accuracy**.
   - Last-Turn Localized Control: **$0.9235$ Macro-F1** / **$92.38\%$ Accuracy**.
   - **Sufficiency Gap:** Widens to **$+0.0384$ (+3.84%)**, proving authentic conversational trajectory dependence.

---

### Track 4: Compiling the Final Report from Source

The final report was written using LaTeX and MiKTeX/TeX Live with native TikZ vector diagrams. To recompile the document locally:

```bash
cd Final-Report

# Using latexmk (recommended)
latexmk -pdf template.tex

# Or using pdflatex + bibtex directly:
pdflatex template.tex
bibtex template
pdflatex template.tex
pdflatex template.tex
```

The resulting PDF will be generated at [`Final-Report/Report_G10.pdf`](Final-Report/Report_G10.pdf) (or `template.pdf` by default when building without `-jobname=Report_G10`). Alternatively, zip the `Final-Report/` folder and upload it directly to [Overleaf](https://www.overleaf.com/) (select compiler: **pdfLaTeX**, TeX Live version: 2023 or later).

---

## 🌐 Demonstration Applications (Havn Platform)

The project includes two interactive web applications demonstrating real-time inference on deployed models, accessible at:

1. **Charity Persuasion Application:**  
   🔗 [https://intentionalysis-persuasion.vercel.app](https://intentionalysis-persuasion.vercel.app)  
   *Simulates donor-fundraiser chat where the AI observer monitors donor commitment probability live, detects rhetorical strategies deployed by the fundraiser, and flags manipulative pressure.*

2. **Commerce Negotiation Application:**  
   🔗 [https://intentionalysis-buyer-seller.vercel.app](https://intentionalysis-buyer-seller.vercel.app)  
   *Simulates buyer-merchant e-commerce negotiation where the AI observer computes non-monotonic buyer commitment trajectories and predicts deal closing probability.*

---

## 👥 Team Members & Contact

**Group 10**, Department of Computer Science and Engineering,  
Bangladesh University of Engineering and Technology (BUET), Dhaka, Bangladesh.

| Name | Student ID | Academic Email / GitHub |
| :--- | :---: | :--- |
| **Arnob Biswas** | 2105015 | `2105015@ug.cse.buet.ac.bd` |
| **Nawriz Ahmed Turjo** | 2105032 | `2105032@ug.cse.buet.ac.bd` |
| **Abhishek Roy** | 2105033 | `2105033@ug.cse.buet.ac.bd` · [@Abhishek12105021](https://github.com/Abhishek12105021) |
| **Monjur Hossain Khan** | 2105043 | `2105043@ug.cse.buet.ac.bd` |
| **Shams Hossain Simanto** | 2105048 | `2105048@ug.cse.buet.ac.bd` |

**Academic Supervisor:**  
**Dr. Md. Shariful Islam Bhuyan**  
Associate Professor, Department of Computer Science and Engineering  
Bangladesh University of Engineering and Technology (BUET)  
Email: `sharifulbhuyan@cse.buet.ac.bd`

---

## 📜 Citation

If you find this codebase, benchmark datasets, or the Antiphony architecture helpful in your research, please cite:

```bibtex
@mastersthesis{antiphony2026buet,
  title        = {Antiphony: Dual-Perspective Modeling of Persuasion and Commitment in Asymmetric Dialogue},
  author       = {Biswas, Arnob and Turjo, Nawriz Ahmed and Roy, Abhishek and Khan, Monjur Hossain and Simanto, Shams Hossain},
  school       = {Department of Computer Science and Engineering, Bangladesh University of Engineering and Technology (BUET)},
  year         = {2026},
  type         = {Undergraduate Capstone Thesis (CSE 450)},
  note         = {Supervised by Dr. Md. Shariful Islam Bhuyan. Available at: https://github.com/Abhishek12105021/CSE-450-Persusaion-For-Good}
}
```

---
*Department of Computer Science and Engineering, Bangladesh University of Engineering and Technology (BUET), Dhaka, Bangladesh.*
