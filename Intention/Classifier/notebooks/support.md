Searched for "class "
Viewed capstone-v8-hierarchical-augplus.ipynb:1-200
Searched for "HierarchicalDialogueClassifier"
Searched for "hierarchical"
Searched for "hierarchical"
Listed directory Week-10
Listed directory notebooks
Viewed architecture-v8.md:1-122
Viewed architecture-v6.md:1-189
Viewed capstone-v8-hierarchical-augplus.ipynb:800-1100
Viewed capstone-v8-hierarchical-augplus.ipynb:1100-1400

The architecture in [capstone-v8-hierarchical-augplus.ipynb](capstone-v8-hierarchical-augplus.ipynb) combines a **Hierarchical Dialogue Transformer** with an **Augmentation Plus** pipeline for multi-task donation-intent classification.

---

## 1. Overall System Architecture

The notebook solves a two-task classification problem on conversation transcripts (from the *Persuasion for Good* dataset):
1. **Binary Intent Classification**: Predicting whether the persuadee agreed to donate (`no`, `yes`).
2. **Modifier Classification**: Predicting the nuance/conditionality of donation (`none`, `deferred`, `conditional`).

### End-to-End Architectural Flow

```
Raw Dialogue Transcript
   │
   ▼
[1. Turn Splitting & Preprocessing] ──> Regex-based extraction of (Speaker, Utterance) turns
   │
   ▼
[2. Hierarchical Batching] ───────────> Dynamic 3D Tensor: [Batch B, Utterances U, Tokens L]
   │
   ▼
[3. Shared Utterance Encoder] ────────> Flatten [B*U, L] -> RoBERTa / DeBERTa-v3 / TOD-BERT
   │                                    Masked Mean Pooling -> Turn vectors [B, U, H]
   ▼
[4. Role & Position Injection] ───────> Turn Vecs + Role Embeddings + Turn Position Embeddings
   │
   ▼
[5. Dialogue Transformer] ────────────> 4-Layer Transformer Encoder attending over turns [B, U, H]
   │
   ▼
[6. Turn-Level Attention Pooling] ────> Learned attention weights over turns -> Shared Vector [B, H]
   │
   ├────────────────────────────────────┐
   ▼                                    ▼
[Binary Head]                   [Cascaded Modifier Head]
 Linear(H -> 2)                  Linear(H + 2 -> H/2) -> GELU -> Dropout -> Linear(H/2 -> 3)
   │                                    │
   ▼                                    ▼
binary_logits                    modifier_logits
```

---

## 2. Key Architectural Components

### A. Preprocessing & Utterance Splitting
* **`split_into_utterances()`**: Uses regex matching (`\[Persuader\]|\[Persuadee\]`) by character positions (handling unspaced newlines).
* Preserves speaker roles (`ROLE_PERSUADER = 0`, `ROLE_PERSUADEE = 1`, `ROLE_PAD = 2`).
* Truncation policy: Retains the **last** 32 turns (`max_utterances=32`) if exceeded, preserving the crucial closing phase where decisions are made.

### B. Level 1: Shared Utterance Encoder
* **Backbones**: Evaluated across `roberta-base`, `microsoft/deberta-v3-base`, and `TOD-BERT-JNT-V1`.
* **Single Batched Forward Pass**: Reshapes the `[B, U, L]` tensor into `[B * U, L]`. All turns across all dialogues in the batch are processed in one GPU forward pass.
* **Masked Mean-Pooling**: Averages token hidden states across valid tokens for each turn:
  $$\mathbf{u}_i = \frac{\sum_{t=1}^{L} \mathbf{h}_{i,t} \cdot m_{i,t}}{\sum_{t=1}^{L} m_{i,t}} \quad \in \mathbb{R}^H$$
* Reshaped back to `[B, U, H]`.

### C. Speaker-Role & Turn-Position Embeddings
Unlike flat models that inject roles at the token level:
* **Role Embedding** (`nn.Embedding(3, H)`): Added to each turn vector according to whether the Persuader or Persuadee spoke.
* **Turn Position Embedding** (`nn.Embedding(max_utterances, H)`): Injects conversational order ($1^{\text{st}}$ turn, $2^{\text{nd}}$ turn, ..., $U^{\text{th}}$ turn) into the turn vectors.

### D. Level 2: The Dialogue Transformer
* A 4-layer Transformer Encoder (`nn.TransformerEncoder`, 8 attention heads, `dim_feedforward=4H`, GELU activation, `batch_first=True`).
* Operates across the sequence of turn vectors `[B, U, H]` with `src_key_padding_mask = ~utt_mask` to prevent padding turns from corrupting real turns.

### E. Turn-Level Attention Pooling
Instead of simple mean-pooling or taking the last turn vector, a learned attention scoring layer computes how informative each turn is:
$$\text{score}_i = \mathbf{w}_2^\top \tanh(\mathbf{W}_1 \mathbf{h}_i)$$
$$\alpha_i = \frac{\exp(\text{score}_i)}{\sum_{j=1}^U \exp(\text{score}_j)}$$
$$\mathbf{z}_{\text{shared}} = \sum_{i=1}^U \alpha_i \mathbf{h}_i \quad \in \mathbb{R}^H$$

### F. Cascaded Multi-Task Heads
* **Binary Head**: $\mathbf{y}_{\text{bin}} = \mathbf{W}_{\text{bin}} \mathbf{z}_{\text{shared}} + \mathbf{b}_{\text{bin}}$
* **Cascaded Modifier Head**: Takes the concatenated input $[\mathbf{z}_{\text{shared}} \, ; \, \text{softmax}(\mathbf{y}_{\text{bin}}).\text{detach()}] \in \mathbb{R}^{H+2}$ into a 2-layer MLP.

### G. Optimization & Loss Functions
* **Class-Balanced Focal Loss** (Cui et al., 2019): Uses effective sample weighting $\frac{1 - \beta}{1 - \beta^n}$ and focusing parameter $\gamma = 2.0$ to handle severe minority imbalance (`conditional`, `deferred`).
* **Supervised Contrastive Loss** (Khosla et al., 2020): Applied to $\mathbf{z}_{\text{shared}}$ in-batch to pull embeddings of matching intent classes together and push differing classes apart.

---

## 3. What is a Dialogue Transformer?

A **Dialogue Transformer** (also called an **Inter-Utterance Transformer** or **Discourse-Level Transformer**, popularized in hierarchical models like HiTrans, HAN, and HRED variants) is a Transformer architecture specifically designed to model **relationships between dialogue turns**, rather than relationships between raw words/tokens.

```
Standard (Flat) Transformer:
[Token 1] ───< Self-Attention over Words >─── [Token 2] ─── ... ─── [Token 512] (Truncates long dialogues)

Hierarchical Dialogue Transformer:
[Turn 1 Vector] ───< Self-Attention over Discourse/Turns >─── [Turn 2 Vector] ─── ... ─── [Turn 32 Vector]
```

### Why a Dialogue Transformer is Used (Core Advantages):

1. **Overcomes Truncation Bottlenecks**:
   * A standard flat BERT/RoBERTa has a token limit (e.g., 256 or 512 tokens). In this persuasion dataset, conversations average ~344 words (some exceeding 1,200 words). Flat tokenizers truncate the end of the conversation where the donate decision actually occurs.
   * A Dialogue Transformer splits the sequence into turns (e.g., 32 turns of 64 tokens each = 2,048 tokens total capacity) without hitting memory limits.

2. **Hierarchical Discourse Modeling**:
   * **Intra-turn level**: Understands local semantics within a turn (e.g., *"I might do it later if my paycheck clears"*).
   * **Inter-turn level (Dialogue Transformer)**: Understands global conversational dynamics across turns:
     * How the persuadee responds to specific persuasion tactics across time.
     * Stance transitions (e.g., shifting from skepticism in Turn 4 to agreement in Turn 14).
     * Distinguishing the persuasion pitch from the final commitment.

3. **Computational Efficiency**:
   * Self-attention over a flat sequence of $N = U \times L$ tokens costs $O((U \cdot L)^2)$.
   * A hierarchical approach costs $O(U \cdot L^2)$ for the utterance encoder plus $O(U^2)$ for the dialogue transformer. Because $U \ll N$, this is substantially lighter on memory and computation.