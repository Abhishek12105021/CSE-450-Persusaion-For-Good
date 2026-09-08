import os
import json
import random

DATASET_DIR = os.path.dirname(os.path.abspath(__file__))
TARGET_FILE = os.path.join(DATASET_DIR, "english_buyer_seller_dialogues2.json")
SEED_FILE = os.path.join(DATASET_DIR, "english_buyer_seller_dialogues.json")

# 1. Product Knowledge Base
PRODUCTS = [
    {
        "name": "Keychron Q1 Pro Custom Keyboard", "category": "Computing & Peripherals", "price": 18500,
        "specs": [
            ("Does it support wireless 2.4GHz dongle or only Bluetooth 5.1?", "The Q1 Pro operates on Bluetooth 5.1 and Type-C wired mode. It does not come with a 2.4GHz dongle."),
            ("What type of switches does it come with?", "It comes pre-installed with Keychron K Pro Banana tactile switches, but it's fully hot-swappable."),
            ("Is the body plastic or metal?", "It has a premium full CNC machined aluminum body."),
            ("Does it support QMK/VIA for key remapping?", "Yes, it fully supports QMK and VIA right out of the box for custom keymaps and macros.")
        ]
    },
    {
        "name": "Sony WH-1000XM5 Wireless Headphones", "category": "Audio & Visual Gear", "price": 32000,
        "specs": [
            ("How is the active noise cancellation compared to the XM4?", "The XM5 uses two processors and 8 microphones for significantly improved noise cancellation, especially for high-frequency sounds."),
            ("Does it support multi-point Bluetooth connection?", "Yes, you can connect it to two devices simultaneously, like your phone and laptop."),
            ("What is the battery life like with ANC on?", "You get up to 30 hours of battery life with noise cancellation turned on."),
            ("Can I use them wired if the battery dies?", "Yes, it comes with a 3.5mm headphone cable for passive wired listening.")
        ]
    },
    {
        "name": "Garmin Forerunner 265 GPS Watch", "category": "Sports & Fitness", "price": 46500,
        "specs": [
            ("Does this model have the AMOLED screen?", "Yes, the Forerunner 265 features a bright, vibrant AMOLED touchscreen display."),
            ("How accurate is the GPS in the city?", "It uses Multi-band GNSS technology, providing excellent accuracy even near tall buildings or dense tree cover."),
            ("Can I store music directly on the watch?", "Absolutely, it has 8GB of internal storage so you can download Spotify playlists for phone-free running."),
            ("What is the battery life in smartwatch mode?", "It lasts up to 13 days in smartwatch mode, or up to 20 hours in GPS mode.")
        ]
    },
    {
        "name": "Breville Barista Express Espresso Machine", "category": "Home & Kitchen Appliances", "price": 78000,
        "specs": [
            ("Does it have a built-in grinder?", "Yes, it has an integrated precision conical burr grinder with dose control."),
            ("What size is the portafilter?", "It comes with a standard 54mm stainless steel portafilter."),
            ("Can I manually texture milk for latte art?", "Yes, the powerful steam wand allows you to hand-texture microfoam milk perfect for latte art."),
            ("Is it a single or dual boiler?", "It uses a single Thermocoil heating system, meaning you brew espresso and steam milk sequentially, not simultaneously.")
        ]
    },
    {
        "name": "Fujifilm X-T30 II Mirrorless Camera", "category": "Audio & Visual Gear", "price": 98000,
        "specs": [
            ("Does this include a kit lens?", "Yes, this package includes the XC 15-45mm OIS PZ lens."),
            ("Does it have in-body image stabilization (IBIS)?", "No, the X-T30 II does not have IBIS. Stabilization relies on OIS-equipped lenses like the one included."),
            ("How many film simulation modes does it have?", "It features 18 classic Fujifilm film simulation modes, including Classic Neg and Eterna."),
            ("Can it shoot 4K video?", "Yes, it records oversampled 4K/30p video with no crop.")
        ]
    },
    {
        "name": "Samsung T7 Shield 2TB Portable SSD", "category": "Computing & Peripherals", "price": 22500,
        "specs": [
            ("Is it rugged and drop-resistant?", "Yes, it has a tough rubberized exterior and can survive drops from up to 3 meters."),
            ("What are the read and write speeds?", "It delivers sequential read/write speeds of up to 1050/1000 MB/s via USB 3.2 Gen 2."),
            ("Can I record Apple ProRes directly to it from an iPhone 15 Pro?", "Yes, it is fully compatible for direct ProRes 4K recording from the iPhone 15 Pro."),
            ("Is it water resistant?", "It has an IP65 rating for water and dust resistance, making it great for outdoor shoots.")
        ]
    },
    {
        "name": "Dyson Purifier Cool TP07", "category": "Home & Kitchen Appliances", "price": 68000,
        "specs": [
            ("Does it cool the room like an AC?", "No, it is a fan and purifier. It circulates purified air but does not have a compressor to lower the room temperature."),
            ("What kind of filters does it use?", "It uses a fully sealed HEPA H13 standard filter that captures 99.97% of particles as small as 0.3 microns."),
            ("Does it connect to WiFi?", "Yes, you can control it and monitor air quality in real-time using the MyDyson app via WiFi."),
            ("How far does it oscillate?", "It features adjustable oscillation up to 350 degrees to project air across the whole room.")
        ]
    },
    {
        "name": "Viofo A129 Pro Duo 4K Dash Cam", "category": "Automotive & Riding Gear", "price": 23500,
        "specs": [
            ("Is the rear camera also 4K?", "No, the front camera records in true 4K (Sony Exmor R), while the rear camera records in 1080p (Sony Starvis)."),
            ("Does it record while parked?", "Yes, but you need to purchase and install the optional HK3 Hardwire Kit to enable buffered parking mode."),
            ("Does it have built-in WiFi to download videos?", "Yes, it features dual-band (2.4GHz & 5GHz) WiFi for fast video transfers to your phone."),
            ("Does it come with an SD card?", "No, the MicroSD card must be purchased separately. We recommend High Endurance cards.")
        ]
    }
]

# 2. Phrase Banks
GREETINGS_BUYER = [
    "Hi there, is the {product} available in ready stock?",
    "Hello! I saw your post regarding the {product}. Do you have it?",
    "Hey, I am interested in purchasing the {product}. Is it available?",
    "Good afternoon, I am looking for the {product}. Can you confirm stock?",
    "Hi, I want to buy the {product}. Let me know if it's available.",
    "Hello, is the {product} currently in stock?"
]

GREETINGS_SELLER = [
    "Hello! Yes, the {product} is available in our ready stock.",
    "Hi there! Thanks for reaching out. We do have it available.",
    "Greetings! Yes, we have brand new units in stock.",
    "Hello sir/ma'am. Yes, it's currently available for immediate delivery.",
    "Hi! Absolutely, we have it ready for you."
]

CONDITION_Q_BUYER = [
    "Awesome. Before we proceed, is it completely brand new and factory sealed?",
    "Great. What condition is it in? Is it 100% intact?",
    "Good to know. Can you confirm if this is official brand new stock with warranty?",
    "Perfect. Just confirming, this is a completely sealed, unopened unit right?",
    "Nice. Does it come intact with the original factory seal?"
]

CONDITION_A_SELLER = [
    "Yes, it is 100% official brand new, factory sealed with all accessories.",
    "Absolutely. It is completely intact, unopened, and comes with a 1-year official warranty.",
    "Yes sir, we only deal in genuine, factory-sealed products. It's completely brand new.",
    "Of course. It's an official global version, sealed box, with full warranty.",
    "Yes, it is guaranteed brand new and sealed. You'll be the first to open it."
]

PRICE_Q_BUYER = [
    "Alright. So what is the final price for this?",
    "Okay, that sounds good. How much are you asking for it?",
    "Understood. Could you let me know the current price?",
    "Great. What's your best price for this item?",
    "Thanks. How much does it cost in total?"
]

PRICE_A_SELLER = [
    "The current official price is {price} BDT.",
    "Our selling price for this unit is {price} BDT.",
    "The item is priced at {price} BDT.",
    "For the genuine sealed unit, the price is {price} BDT.",
    "We are currently offering it for {price} BDT."
]

DISCOUNT_Q_BUYER = [
    "That's a bit steep. Can you offer any discount on that?",
    "Any chance you can lower the price a bit? Maybe {discount_price} BDT?",
    "I've seen it slightly cheaper elsewhere. Can you do {discount_price} BDT?",
    "Could you give a small discount? My budget is closer to {discount_price} BDT.",
    "Is the price fixed or negotiable? I was hoping for {discount_price} BDT."
]

DISCOUNT_REJECT_SELLER = [
    "I apologize, but {price} BDT is our final fixed price. Margins on official products are very tight.",
    "Sorry sir, we cannot match that. Our price of {price} BDT is already discounted for genuine stock.",
    "Unfortunately, the price is fixed at {price} BDT. We guarantee the authenticity and warranty, which cheaper stores might compromise on.",
    "We really can't go that low. The best we can do is the stated {price} BDT. It's a premium item."
]

DISCOUNT_ACCEPT_SELLER = [
    "Since you are confirming today, I can meet you in the middle at {middle_price} BDT.",
    "I can't do {discount_price}, but as a special offer for a quick deal, I can offer {middle_price} BDT.",
    "Margin is tight, but I want to make this sale. I'll agree to {middle_price} BDT.",
    "Alright, I can give a small concession. Final price {middle_price} BDT. Deal?"
]

DELIVERY_Q_BUYER = [
    "Okay, how does the delivery process work?",
    "What are the delivery options and charges?",
    "How fast can you deliver it to my address?",
    "I need it delivered to my home. What's the procedure?",
    "Alright. Do you do home delivery? And what is the fee?"
]

DELIVERY_A_SELLER = [
    "We offer home delivery all over Bangladesh via Steadfast/Pathao. Inside Dhaka is 100 BDT (24 hours), Outside Dhaka is 160 BDT (48-72 hours).",
    "Delivery is 100 BDT inside Dhaka and 160 BDT outside. We dispatch immediately upon order confirmation.",
    "We use premium courier services. It takes 1 day for Dhaka (100 BDT) and 2-3 days outside (160 BDT).",
    "Delivery charge is 100 BDT for Dhaka, 160 BDT outside. Packages are fully insured."
]

ADVANCE_POLICY_SELLER = [
    "To confirm the order, we require a small 500 BDT advance via bKash to cover the courier booking fee. The rest is Cash on Delivery.",
    "We just need 500 BDT sent to our merchant bKash as a security deposit for the courier. The remaining amount will be collected as COD.",
    "Since it's a high-value item, our policy requires a 500 BDT advance payment. You can pay the rest to the delivery man.",
    "For order confirmation, a 500 BDT advance via bKash is mandatory. The balance is full Cash on Delivery (COD)."
]

ADVANCE_DOUBT_BUYER = [
    "I am not comfortable sending an advance. I've had bad experiences with pages taking advance and blocking. Can you do full COD?",
    "Why the advance? I want 100% Cash on Delivery without any prior payment.",
    "I prefer paying everything when I have the product in my hands. Can we skip the advance?",
    "Is the advance strictly necessary? I'd rather do full COD."
]

ADVANCE_REASSURE_SELLER = [
    "I completely understand your concern. The advance simply ensures you are a serious buyer and covers our return shipping risk if the parcel is rejected. You can check our page reviews and physical shop address for peace of mind.",
    "We sympathize, but this is a strict company policy for items over 10,000 BDT to prevent fake orders. You can verify our trade license and physical store in Multiplan Center.",
    "Sir, it's just 500 BDT for courier security. We have a solid 5-year track record and thousands of reviews. We cannot bypass this policy, unfortunately.",
    "It is standard procedure to avoid fake courier requests. We offer an open-box inspection in front of the rider before you pay the remaining COD amount."
]

AGREE_TO_ADVANCE_BUYER = [
    "Alright, that makes sense. I will send the 500 BDT advance.",
    "Okay, I understand. I'll trust your page this time. Sending the advance now.",
    "Fair enough. I'll send the 500 BDT to confirm the booking.",
    "Sure, I'll pay the advance. Please share your bKash number."
]

EXPLICIT_REJECT_BUYER = [
    "No, I won't pay a single taka in advance. If you can't do full COD, then cancel my order.",
    "Sorry, I don't trust Facebook pages with advance payments. I'll buy from a physical shop. Cancel it.",
    "That doesn't work for me. I refuse to pay the advance. Forget it.",
    "Never mind then. If there's no full COD, I am not interested."
]

DEFER_BUYER = [
    "Thanks for all the detailed info. I need to think about it for a bit. I'll let you know.",
    "I appreciate the answers. Let me discuss this with my family/friends and I'll get back to you tomorrow.",
    "Understood. I have to check my budget at the end of the month before committing. I'll message you later.",
    "I'll have to compare this with a few other models first. Will contact you if I decide to buy."
]

ADDRESSES = [
    "House 14, Road 3, Dhanmondi, Dhaka",
    "Apartment 6B, House 42, Road 11, Banani, Dhaka",
    "Sector 7, Road 18, House 5, Uttara, Dhaka",
    "Agrabad Commercial Area, GEC Circle, Chattogram",
    "Zindabazar, Lamabazar Road, Sylhet",
    "House 102, Road 5, Block B, Bashundhara R/A, Dhaka",
    "Kandirpar, Victoria College Road, Cumilla",
    "Building 24, Road 8, Mirpur DOHS, Dhaka",
    "Shaheb Bazar, Master Para, Rajshahi"
]
PHONES = ["01712349911", "01819876543", "01923456789", "01734567890", "01687654321", "01711223388", "01822334455"]

# 3. State Machine Generator
def generate_dialogue(dialogue_id, outcome):
    prod = random.choice(PRODUCTS)
    base_price = prod["price"]
    is_dhaka = random.choice([True, False, True, True]) # 75% Dhaka
    delivery_fee = 100 if is_dhaka else 160
    
    turns = []
    turn_counter = 1
    
    def add_turn(role, text, intent):
        nonlocal turn_counter
        turns.append({
            "turn_id": turn_counter,
            "role": role,
            "text": text,
            "normalized_intent": intent
        })
        turn_counter += 1

    # --- Phase 1: Greeting & Condition ---
    add_turn("Buyer", random.choice(GREETINGS_BUYER).format(product=prod["name"]), "INQUIRE_INFO")
    add_turn("Merchant", random.choice(GREETINGS_SELLER).format(product=prod["name"]), "INFORM_PRODUCT")
    add_turn("Buyer", random.choice(CONDITION_Q_BUYER), "EXPRESS_DOUBT")
    add_turn("Merchant", random.choice(CONDITION_A_SELLER), "REASSURE_CUSTOMER")

    # --- Phase 2: Specs ---
    # Pick 2 or 3 random specs to ask about
    num_specs = random.choice([2, 3])
    specs_to_ask = random.sample(prod["specs"], num_specs)
    
    for i, (q, a) in enumerate(specs_to_ask):
        if i == 0:
            prefix = "I had a technical question. "
        elif i == num_specs - 1:
            prefix = "One last question about the specs. "
        else:
            prefix = random.choice(["Also, ", "Another thing: ", "I see. And "])
            
        add_turn("Buyer", prefix + q, "INQUIRE_INFO")
        add_turn("Merchant", a, "INFORM_PRODUCT")

    # If dropout happens early (INQUIRY_DROPOUT), exit here sometimes
    if outcome == "INQUIRY_DROPOUT" and random.random() < 0.3:
        add_turn("Buyer", "I see. Unfortunately that spec doesn't meet my requirements. Thanks anyway.", "INQUIRE_INFO")
        add_turn("Merchant", "No problem! Let us know if you need anything else.", "INFORM_PRODUCT")
        return turns, "no", "INQUIRY_DROPOUT", "Buyer dropped out early due to technical specification mismatch."

    # --- Phase 3: Pricing ---
    add_turn("Buyer", random.choice(PRICE_Q_BUYER), "INQUIRE_PRICE")
    add_turn("Merchant", random.choice(PRICE_A_SELLER).format(price=f"{base_price:,}"), "INFORM_PRICE")

    # If DEFERRED_CONSIDERATION, mostly exit here
    if outcome == "DEFERRED_CONSIDERATION":
        add_turn("Buyer", random.choice(DEFER_BUYER), "DEFER_DECISION")
        add_turn("Merchant", "Sure sir, take your time! We are always here when you are ready.", "REASSURE_CUSTOMER")
        return turns, "no", "DEFERRED_CONSIDERATION", "Buyer deferred decision after learning the price and specs."

    # Negotiation
    discount_amount = random.randint(1000, 3000)
    discount_price = base_price - discount_amount
    middle_price = base_price - (discount_amount // 2)
    
    add_turn("Buyer", random.choice(DISCOUNT_Q_BUYER).format(discount_price=f"{discount_price:,}"), "NEGOTIATE_PRICE")
    
    if outcome == "INQUIRY_DROPOUT":
        add_turn("Merchant", random.choice(DISCOUNT_REJECT_SELLER).format(price=f"{base_price:,}"), "COUNTER_OFFER")
        add_turn("Buyer", "That's too high for me. I'll have to pass and buy from Daraz.", "NEGOTIATE_PRICE")
        add_turn("Merchant", "We understand. We don't compromise on quality or warranty. Have a good day.", "INFORM_PRODUCT")
        return turns, "no", "INQUIRY_DROPOUT", "Buyer abandoned dialogue after merchant refused discount."
        
    # Merchant compromises
    add_turn("Merchant", random.choice(DISCOUNT_ACCEPT_SELLER).format(discount_price=f"{discount_price:,}", middle_price=f"{middle_price:,}"), "COUNTER_OFFER")
    add_turn("Buyer", f"Alright, {middle_price:,} BDT sounds fair. I'll take it.", "ACCEPT_OFFER")

    # --- Phase 4: Delivery & Advance ---
    add_turn("Buyer", random.choice(DELIVERY_Q_BUYER), "INQUIRE_INFO")
    add_turn("Merchant", random.choice(DELIVERY_A_SELLER), "INFORM_PRICE")
    
    # Merchant states advance policy
    add_turn("Merchant", random.choice(ADVANCE_POLICY_SELLER), "INFORM_PRODUCT")
    
    # Buyer expresses doubt
    add_turn("Buyer", random.choice(ADVANCE_DOUBT_BUYER), "EXPRESS_DOUBT")
    add_turn("Merchant", random.choice(ADVANCE_REASSURE_SELLER), "REASSURE_CUSTOMER")

    if outcome == "EXPLICIT_REJECTION":
        add_turn("Buyer", random.choice(EXPLICIT_REJECT_BUYER), "EXPLICIT_REJECTION")
        add_turn("Merchant", "Understood sir. Your order request has been cancelled. Good luck.", "CONFIRM_TRANSACTION")
        return turns, "no", "EXPLICIT_REJECTION", "Buyer explicitly rejected mandatory advance fee and walked away."

    # --- Phase 5: Closing (PURCHASE_COMMITTED) ---
    add_turn("Buyer", random.choice(AGREE_TO_ADVANCE_BUYER), "COMMIT_PURCHASE")
    
    bkash = f"017{random.randint(10000000, 99999999)}"
    add_turn("Merchant", f"Thank you for understanding! Please send 500 BDT to {bkash} (Merchant) and share the TrxID.", "CONFIRM_TRANSACTION")
    
    trxid = f"BK{random.randint(10,99)}X{random.randint(100,999)}P"
    addr = random.choice(ADDRESSES)
    phone = random.choice(PHONES)
    add_turn("Buyer", f"Sent 500 BDT. TrxID is {trxid}. Please deliver to: {addr}. Mobile: {phone}.", "COMMIT_PURCHASE")
    
    add_turn("Merchant", f"Payment received and verified. Your order is confirmed. The remaining {middle_price - 500 + delivery_fee:,} BDT will be collected on delivery.", "CONFIRM_TRANSACTION")

    return turns, "yes", "PURCHASE_COMMITTED", "Buyer completed negotiation, accepted advance policy, and committed to purchase."


def main():
    # Load 155 seed dialogues
    with open(SEED_FILE, "r", encoding="utf-8") as f:
        corpus = json.load(f)
        
    print(f"Loaded {len(corpus)} seed dialogues.")

    planned_outcomes = (
        ["PURCHASE_COMMITTED"] * 165 +
        ["DEFERRED_CONSIDERATION"] * 95 +
        ["INQUIRY_DROPOUT"] * 75 +
        ["EXPLICIT_REJECTION"] * 10
    )
    random.seed(104) # fresh seed
    random.shuffle(planned_outcomes)
    
    assert len(planned_outcomes) == 345

    generated_count = 0
    total_turns = 0

    for i, outcome in enumerate(planned_outcomes):
        d_id = 156 + i
        turns, intent, outcome_cat, reason = generate_dialogue(d_id, outcome)
        
        dialogue = {
            "dialogue_id": f"ENG_{d_id:03d}",
            "source_file": "advanced_procedural_generator.json",
            "source_model": "antigravity-advanced-state-machine",
            "original_id": i + 1,
            "product": "Assorted Tech & Gear",
            "category": "Mixed",
            "archetype": "Organic Sim",
            "language_style": "Pure English",
            "labels": {
                "buying_intent": intent,
                "outcome_category": outcome_cat,
                "reason": reason
            },
            "turn_count": len(turns),
            "turns": turns
        }
        corpus.append(dialogue)
        generated_count += 1
        total_turns += len(turns)

    print(f"Generated {generated_count} advanced dialogues.")
    print(f"Average turns per generated dialogue: {total_turns / generated_count:.2f}")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        json.dump(corpus, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully saved {len(corpus)} total dialogues to {TARGET_FILE}.")

if __name__ == "__main__":
    main()
