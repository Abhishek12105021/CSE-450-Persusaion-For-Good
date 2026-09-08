# Dataset Statistics: 500 English Buyer-Seller Intention Dialogues

Comprehensive statistics and metadata for the complete corpus: [`english_buyer_seller_dialogues.json`](file:///e:/3-2/Capstone%20Project/Dataset/english_buyer_seller_dialogues.json).

Generated using the **Hybrid Dual-Level Intention Modeling Architecture** designed for Capstone Group 10.

---

## 1. High-Level Summary Metrics

| Metric | Value | Notes |
| :--- | :---: | :--- |
| **Total Dialogues** | **500** | 155 from benchmark seed models + 345 context-diverse synthetic |
| **Total Turns** | **4,239** | Fully parsed, cleaned, and role-standardized |
| **Buyer Turns** | **2,149** | 50.7% of all turns |
| **Merchant Turns** | **2,090** | 49.3% of all turns |
| **Mean Turns / Dialogue** | **8.48** | Range: 6 to 18 turns |
| **Median Turns / Dialogue** | **8.00** | Balanced multi-turn conversations |
| **Unique Products** | **58** | Electronics, Studio Audio, Home Tech, Ergonomics, Outdoor, Riding Gear, Luxury |
| **Product Categories** | **16** | Comprehensive commercial coverage |
| **Archetypes Covered** | **19** | Realistic buyer persona profiles |

---

## 2. Source Model & Generation Composition

| Source Partition | Generator / Model | Total Dialogues | Percentage |
| :--- | :--- | :---: | :---: |
| **Benchmark Seed (Claude)** | Claude Opus 4.5 | 19 | 3.8% |
| **Benchmark Seed (Qwen)** | Qwen 2.5 72B | 40 | 8.0% |
| **Benchmark Seed (DeepSeek)** | DeepSeek V3.2 | 28 | 5.6% |
| **Benchmark Seed (Gemini)** | Gemini | 34 | 6.8% |
| **Benchmark Seed (GPT)** | GPT | 34 | 6.8% |
| **Context-Diverse Synthetic Expansion** | Gemini 3.8 Pipeline (Local Engine) | 345 | 69.0% |
| **Total Corpus** | — | **500** | **100.0%** |

---

## 3. Ground Truth Intention Distributions

### A. Binary Buying Intent (`buying_intent`)
Direct primary target for binary classification models (paralleling the presentation's commitment head):

| Label | Count | Percentage | Description |
| :---: | :---: | :---: | :--- |
| **`no`** | 265 | **53.0%** | Buyer did not commit to purchase (ghosted, deferred, or abandoned) |
| **`yes`** | 235 | **47.0%** | Buyer committed to purchase (paid, shared TrxID, provided address, or finalized order) |

> [!TIP]
> **Ideal 53:47 Balance**: Highly resistant to majority-class baseline collapse (unlike the donation dataset which had 72.6% `yes`).

---

### B. Distinct Outcome Categories (`outcome_category`)
Multi-class target representing the granular resolution state of each negotiation:

| Category | Count | Percentage | Key Characteristics & Linguistic Cues |
| :--- | :---: | :---: | :--- |
| **`PURCHASE_COMMITTED`** | 235 | **47.0%** | Sent bKash/Nagad payment, shared transaction ID, confirmed shipping address & phone, or explicitly ordered. |
| **`DEFERRED_CONSIDERATION`** | 142 | **28.4%** | Postponed decision: *"Let me think about it"*, *"Need to discuss with wife"*, *"Will message later"*, soft ghosting. |
| **`INQUIRY_DROPOUT`** | 118 | **23.6%** | Interaction stopped after asking price/specs or reaching a price impasse without reaching agreement. |
| **`EXPLICIT_REJECTION`** | 5 | **1.0%** | Customer demanded refund / rejected advance courier policy (*"Never contact me again"*). |

---

## 4. Archetype vs. Outcome Cross-Tabulation

| Archetype Persona | Total Dialogues | `PURCHASE_COMMITTED` | `DEFERRED_CONSIDERATION` | `INQUIRY_DROPOUT` | `EXPLICIT_REJECTION` | Conversion Rate |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **LowBaller** | 95 | 46 | 30 | 19 | 0 | 48.4% |
| **Skeptic** | 77 | 41 | 31 | 4 | 1 | 53.2% |
| **TrustSeeker** | 63 | 30 | 0 | 30 | 3 | 47.6% |
| **Ghoster** | 59 | 0 | 55 | 4 | 0 | 0.0% |
| **Urgent** | 55 | 53 | 0 | 2 | 0 | **96.4%** |
| **Tech Specs Nerd** | 53 | 27 | 24 | 2 | 0 | 50.9% |
| **DeliveryObsessed** | 33 | 30 | 0 | 3 | 0 | **90.9%** |
| **BulkBuyer** | 30 | 0 | 0 | 30 | 0 | 0.0% |
| **Comparator** | 22 | 0 | 0 | 22 | 0 | 0.0% |
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
| **Total Corpus** | **500** | **235** | **142** | **118** | **5** | **47.0%** |

---

## 5. Turn-Level Intent Taxonomy

### A. Buyer Normalized Intents (2,149 turns)
| Standardized Intent | Turn Count | Prevalence | Primary Definition |
| :--- | :---: | :---: | :--- |
| `INQUIRE_INFO` | 674 | 31.4% | Questions on availability, specifications, condition, warranty, or delivery times. |
| `INQUIRE_PRICE` | 567 | 26.4% | Requesting price quotes, EMI availability, or delivery charges. |
| `COMMIT_PURCHASE` | 303 | 14.1% | Sending payment/TrxID, providing delivery address/phone, or finalizing checkout. |
| `NEGOTIATE_PRICE` | 198 | 9.2% | Bargaining, asking for discounts, comparing competitors' rates. |
| `EXPRESS_DOUBT` | 176 | 8.2% | Concerns about authenticity, counterfeit items, return policy safety. |
| `DEFER_DECISION` | 142 | 6.6% | Explicit hesitation, soft exit (*"let me think"*, *"ask my brother"*). |
| `ACCEPT_OFFER` | 48 | 2.2% | Accepting seller's negotiated price or special offer. |
| `REQUEST_PROOF` | 36 | 1.7% | Demanding photos, IMEI numbers, videos, or lab certificates. |
| `EXPLICIT_REJECTION` | 5 | 0.2% | Active refusal or refund demand. |

---

### B. Merchant Normalized Strategies (2,090 turns)
| Standardized Strategy | Turn Count | Prevalence | Primary Definition |
| :--- | :---: | :---: | :--- |
| `INFORM_PRODUCT` | 661 | 31.6% | Stating product specifications, stock status, features, or compatibility. |
| `INFORM_PRICE` | 470 | 22.5% | Quoting product pricing, delivery costs, or total calculations. |
| `CONFIRM_TRANSACTION` | 383 | 18.3% | Acknowledging order, requesting address/payment details, confirming dispatch. |
| `REASSURE_CUSTOMER` | 296 | 14.2% | Clarifying warranty terms, COD security, return policy, and store authenticity. |
| `COUNTER_OFFER` | 224 | 10.7% | Negotiating, providing compromise discounts, bundle deals, or alternatives. |
| `PROVIDE_PROOF` | 51 | 2.4% | Sending photos, live video, serial numbers, or certification proof. |
| `CREATE_URGENCY` | 5 | 0.2% | Highlighting limited stock, expiring offers, or fast-action incentives. |

---

## 6. Product Category Distribution across the 500 Dialogues

| Product Category | Dialogues | Sample Products Included |
| :--- | :---: | :--- |
| **Computing & Peripherals** | 82 | Keychron K2, LG UltraGear 4K Monitor, MX Master 3S, Wacom Tablet, Anker PowerBank |
| **Audio & Visual Equipment** | 76 | Sony WH-1000XM5, Rode Wireless GO II, DJI Mini 4 Pro Drone, Canon EOS R50, Marshall Stanmore |
| **Home & Kitchen Appliances** | 75 | Philips XXL Air Fryer, Xiaomi Robot Vacuum Mop 2, De'Longhi Espresso Machine, Kent RO Purifier |
| **Sports, Fitness & Outdoor** | 68 | Trek Marlin 7 MTB, Yamaha F310 Guitar, Naturehike 2P Tent, SS Ton English Willow Bat |
| **Automotive & Riding Gear** | 56 | MT Thunder 4 ECE Helmet, 70mai A810 4K Dash Cam, Baseus Tyre Inflator |
| **Workspace & Furniture** | 48 | Sihoo Doro C300 Mesh Chair, Apex Dual-Motor Standing Desk |
| **Luxury & Personal Care** | 45 | Dyson Airwrap Multi-Styler, Tom Ford Oud Wood, Handcrafted Leather Briefcase |
| **Smartphones & Gadgets (Seed)** | 50 | iPhone 15, Smart Watch T500 / Series 8, Blender, Jamdani Saree, Katmon Ghee |
| **Total** | **500** | **58 Distinct Commercial Products** |
