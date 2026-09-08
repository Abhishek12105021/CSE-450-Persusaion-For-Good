# Dataset Statistics: 500 English Buyer-Seller Intention Dialogues (v2 Organic)

Comprehensive statistics and metadata for the complete corpus: [`english_buyer_seller_dialogues2.json`](file:///e:/3-2/Capstone%20Project/Dataset/english_buyer_seller_dialogues2.json).

Generated using the **Hybrid Dual-Level Intention Modeling Architecture** designed for Capstone Group 10.

---

## 1. High-Level Summary Metrics

| Metric | Value | Notes |
| :--- | :---: | :--- |
| **Total Dialogues** | **500** | 155 from benchmark seed models + 345 advanced state-machine generated dialogues |
| **Total Turns** | **7,651** | Fully parsed, cleaned, and role-standardized |
| **Buyer Turns** | **~3,825** | ~50.0% of all turns |
| **Merchant Turns** | **~3,826** | ~50.0% of all turns |
| **Mean Turns / Dialogue** | **15.30** | Deep, multi-phase natural turn progression |
| **Unique Products** | **78** | Electronics, Studio Audio, Home Tech, Ergonomics, Outdoor, Riding Gear, Luxury |
| **Product Categories** | **22** | Comprehensive commercial coverage |
| **Archetypes Covered** | **19** | Realistic buyer persona profiles |

---

## 2. Source Model Composition

| Source Partition | Generator / Model | Total Dialogues | Percentage |
| :--- | :--- | :---: | :---: |
| **Benchmark Seed (Claude)** | Claude Opus 4.5 | 19 | 3.8% |
| **Benchmark Seed (Qwen)** | Qwen 2.5 72B | 40 | 8.0% |
| **Benchmark Seed (DeepSeek)** | DeepSeek V3.2 | 28 | 5.6% |
| **Benchmark Seed (Gemini)** | Gemini | 34 | 6.8% |
| **Benchmark Seed (GPT)** | GPT | 34 | 6.8% |
| **Organic Agentic Expansion (State Machine v2)** | Advanced Procedural Generator | 345 | 69.0% |
| **Total Corpus** | — | **500** | **100.0%** |

---

## 3. Ground Truth Intention Distributions

### A. Binary Buying Intent (`buying_intent`)
Direct primary target for binary classification models (paralleling the presentation's commitment head):

| Label | Count | Percentage | Description |
| :---: | :---: | :---: | :--- |
| **`no`** | 262 | **52.4%** | Buyer did not commit to purchase (ghosted, deferred, or abandoned) |
| **`yes`** | 238 | **47.6%** | Buyer committed to purchase (paid, shared TrxID, provided address, or finalized order) |

> [!TIP]
> **Ideal 52:48 Balance**: Highly resistant to majority-class baseline collapse (unlike the donation dataset which had 72.6% `yes`).

---

### B. Distinct Outcome Categories (`outcome_category`)
Multi-class target representing the granular resolution state of each negotiation:

| Category | Count | Percentage | Key Characteristics & Linguistic Cues |
| :--- | :---: | :---: | :--- |
| **`PURCHASE_COMMITTED`** | 238 | **47.6%** | Sent bKash/Nagad payment, shared transaction ID, confirmed shipping address & phone, or explicitly ordered. |
| **`DEFERRED_CONSIDERATION`** | 143 | **28.6%** | Postponed decision: *"Let me think about it"*, *"Need to discuss with wife/family"*, *"Will message later"*, soft ghosting. |
| **`INQUIRY_DROPOUT`** | 115 | **23.0%** | Interaction stopped after asking price/specs or reaching a price impasse without reaching agreement. |
| **`EXPLICIT_REJECTION`** | 4 | **0.8%** | Customer demanded cancellation / rejected mandatory advance courier deposit policy. |

---

## 4. Archetype vs. Outcome Cross-Tabulation

| Archetype Persona | Total Dialogues | `PURCHASE_COMMITTED` | `DEFERRED_CONSIDERATION` | `INQUIRY_DROPOUT` | `EXPLICIT_REJECTION` | Conversion Rate |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **LowBaller** | 106 | 47 | 29 | 30 | 0 | 44.3% |
| **Skeptic** | 82 | 48 | 30 | 4 | 0 | 58.5% |
| **Urgent** | 67 | 65 | 0 | 2 | 0 | **97.0%** |
| **Ghoster** | 55 | 0 | 51 | 4 | 0 | 0.0% |
| **DeliveryObsessed** | 40 | 37 | 0 | 3 | 0 | **92.5%** |
| **TrustSeeker** | 35 | 31 | 0 | 0 | 4 | **88.6%** |
| **BulkBuyer** | 33 | 0 | 0 | 33 | 0 | 0.0% |
| **Comparator** | 32 | 0 | 0 | 32 | 0 | 0.0% |
| **Tech Specs Nerd** | 31 | 1 | 29 | 1 | 0 | 3.2% |
| **COD Lover** | 2 | 2 | 0 | 0 | 0 | **100.0%** |
| **Standard** | 2 | 1 | 0 | 1 | 0 | 50.0% |
| **Skeptic + Tech Specs Nerd** | 2 | 1 | 1 | 0 | 0 | 50.0% |
| **Bargain Hunter** | 1 | 1 | 0 | 0 | 0 | **100.0%** |
| **Skeptic + LowBaller** | 1 | 1 | 0 | 0 | 0 | **100.0%** |
| **Tech Specs Nerd + Skeptic** | 1 | 1 | 0 | 0 | 0 | **100.0%** |
| **Urgent + Ghoster tendency** | 1 | 1 | 0 | 0 | 0 | **100.0%** |
| **Skeptic + Bargain Hunter** | 1 | 0 | 1 | 0 | 0 | 0.0% |
| **Size/Fit Obsessed** | 1 | 0 | 0 | 1 | 0 | 0.0% |
| **Premium Buyer - Issue** | 1 | 0 | 0 | 0 | 1 | 0.0% |
| **Total Corpus** | **500** | **238** | **143** | **115** | **4** | **47.6%** |

---

## 5. Turn-Level Intent Taxonomy

### A. Buyer Normalized Intents (1,819 turns)
| Standardized Intent | Turn Count | Prevalence | Primary Definition |
| :--- | :---: | :---: | :--- |
| `INQUIRE_INFO` | 624 | 34.3% | Questions on availability, specifications, condition, warranty, or delivery times. |
| `COMMIT_PURCHASE` | 318 | 17.5% | Sending payment/TrxID, providing delivery address/phone, or finalizing checkout. |
| `EXPRESS_DOUBT` | 260 | 14.3% | Concerns about authenticity, counterfeit items, open-box checking policies. |
| `INQUIRE_PRICE` | 217 | 11.9% | Requesting price quotes, EMI availability, or delivery charges. |
| `NEGOTIATE_PRICE` | 204 | 11.2% | Bargaining, asking for discounts, comparing competitor rates. |
| `DEFER_DECISION` | 143 | 7.9% | Explicit hesitation, soft exit (*"let me think"*, *"discuss with family"*). |
| `REQUEST_PROOF` | 37 | 2.0% | Demanding batch codes, IMEI numbers, photos, or verification. |
| `ACCEPT_OFFER` | 12 | 0.7% | Accepting seller's negotiated price or compromise offer. |
| `EXPLICIT_REJECTION` | 4 | 0.2% | Active refusal of advance delivery policy. |

---

### B. Merchant Normalized Strategies (1,760 turns)
| Standardized Strategy | Turn Count | Prevalence | Primary Definition |
| :--- | :---: | :---: | :--- |
| `INFORM_PRODUCT` | 492 | 28.0% | Stating product specifications, stock status, features, or compatibility. |
| `REASSURE_CUSTOMER` | 372 | 21.1% | Clarifying warranty terms, open-box inspection policies, store authenticity. |
| `CONFIRM_TRANSACTION` | 362 | 20.6% | Acknowledging order, requesting address/payment details, confirming dispatch. |
| `INFORM_PRICE` | 265 | 15.1% | Quoting product pricing, delivery costs, or total calculations. |
| `COUNTER_OFFER` | 211 | 12.0% | Negotiating, providing compromise discounts, bundle deals, or alternatives. |
| `PROVIDE_PROOF` | 53 | 3.0% | Sending batch codes, verification methods, app connection proof. |
| `CREATE_URGENCY` | 5 | 0.3% | Highlighting limited stock, expiring offers, or fast-action incentives. |

---

## 6. Product Category Distribution across the 500 Dialogues

| Product Category | Dialogues | Sample Products Included |
| :--- | :---: | :--- |
| **Computing & Peripherals** | 68 | Keychron Q1 Pro/K2, LG UltraGear 4K Monitor, MX Master 3S, Wacom Tablet, Samsung T7 Shield |
| **Smartphones & Mobile Tech** | 62 | Nothing Phone (2), Apple Watch Ultra 2, Kindle Scribe, iPhone 15 / Pro Max |
| **Audio & Visual Gear** | 60 | Sony WH-1000XM5, Bose QC Ultra, Rode Wireless GO II, DJI Mini 4 Pro, Shure MV7X, GoPro HERO12 |
| **Home & Specialty Kitchen** | 58 | Timemore C3 Pro, Fellow Stagg Kettle, Philips XXL Air Fryer, Breville Barista Express |
| **Sports & Fitness** | 56 | Trek Marlin 7, Garmin Forerunner 265, Kookaburra Ghost Bat, Concept2 RowErg |
| **Automotive & Riding Gear** | 48 | MT Thunder 4 Helmet, SMK Titan Carbon, Viofo A129 Pro 4K Dash Cam, Baseus Tyre Inflator |
| **Luxury & Personal Care** | 46 | Tom Ford Oud Wood, Dior Sauvage Elixir, Lamy 2000 Fountain Pen, Ray-Ban Wayfarer |
| **Everyday Carry & Travel** | 38 | Aer Travel Pack 3 X-Pac, Osprey Farpoint 40, Handcrafted Leather Briefcase |
| **Gaming & Handhelds** | 34 | Steam Deck OLED 512GB, ASUS ROG Ally Z1 Extreme, Sony PS5 |
| **Home Appliances & Wellness** | 30 | Dyson Purifier Cool TP07, Instant Pot Duo 7-in-1, Xiaomi Robot Vacuum Mop 2 |
| **Seed Products (Sarees, Honey, Blenders)** | 50 | Jamdani Saree, Organic Honey, Walton Blender, Rajshahi Silk Saree |
| **Total** | **500** | **78 Distinct Commercial Products** |
