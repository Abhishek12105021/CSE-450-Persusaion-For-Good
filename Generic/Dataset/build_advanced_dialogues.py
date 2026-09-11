"""
Compositional Buyer-Seller Dialogue Generator (v2)
===================================================
Replaces the v1 fixed-pipeline state machine, whose 345 dialogues collapsed
into only 10 distinct intent paths and leaked the outcome label through
`turn_count` (87.5% predictable from length alone, 97.1% from the final
intent alone).

v2 changes, in order of effect on label leakage:

  1. PHASE COMPOSITION, not a fixed pipeline. Phases are sampled and
     ordered per dialogue (price-first buyers, spec-circle-backs, advance
     objections raised before negotiation), so intent paths are drawn from
     a combinatorial space instead of 10 hard-coded routes.

  2. LENGTH DECOUPLED FROM OUTCOME. Every outcome can terminate at several
     different phases, and filler phases (small talk, stock re-checks,
     colour/variant questions) are injected independently of outcome. A
     PURCHASE_COMMITTED can run 12 turns; a dropout can run 26.

  3. EXIT POINTS RANDOMISED. Each outcome has multiple plausible exit
     phases with their own closing lines, so the last turn no longer
     identifies the label.

  4. SCHEMA PARITY. Every turn carries `original_intent` alongside
     `normalized_intent`, matching the 155 seed dialogues (v1 emitted
     none, leaving 6,244 turns with a broken schema).

  5. ARCHETYPES drive phase selection and phrasing bank choice, mirroring
     the seed corpus's Skeptic / LowBaller / Ghoster / Urgent / etc.

Output is written to `extended_dataset.json` (seed 155 + generated 345).

Usage:
    python build_advanced_dialogues.py [--n 345] [--seed 104]
"""

import os
import json
import random
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED_FILE = os.path.join(SCRIPT_DIR, "generic_dataset.json")
TARGET_FILE = os.path.join(SCRIPT_DIR, "extended_dataset.json")

# ============================================================
# 1. PRODUCT KNOWLEDGE BASE
# ============================================================
PRODUCTS = [
    {
        "name": "Keychron Q1 Pro Custom Keyboard", "category": "Computing & Peripherals", "price": 18500,
        "specs": [
            ("Does it support wireless 2.4GHz dongle or only Bluetooth 5.1?", "The Q1 Pro operates on Bluetooth 5.1 and Type-C wired mode. It does not come with a 2.4GHz dongle."),
            ("What type of switches does it come with?", "It comes pre-installed with Keychron K Pro Banana tactile switches, but it's fully hot-swappable."),
            ("Is the body plastic or metal?", "It has a premium full CNC machined aluminum body."),
            ("Does it support QMK/VIA for key remapping?", "Yes, it fully supports QMK and VIA right out of the box for custom keymaps and macros."),
            ("What is the keyboard layout size?", "It's a 75% compact layout with a knob, so you keep the function row and arrow keys."),
            ("How heavy is it?", "The full aluminum build weighs around 1.6 kg, so it stays firmly planted on the desk."),
        ],
        "variants": ["Carbon Black", "Silver Grey", "Blue"],
    },
    {
        "name": "Sony WH-1000XM5 Wireless Headphones", "category": "Audio & Visual Gear", "price": 32000,
        "specs": [
            ("How is the active noise cancellation compared to the XM4?", "The XM5 uses two processors and 8 microphones for significantly improved noise cancellation, especially for high-frequency sounds."),
            ("Does it support multi-point Bluetooth connection?", "Yes, you can connect it to two devices simultaneously, like your phone and laptop."),
            ("What is the battery life like with ANC on?", "You get up to 30 hours of battery life with noise cancellation turned on."),
            ("Can I use them wired if the battery dies?", "Yes, it comes with a 3.5mm headphone cable for passive wired listening."),
            ("Does it fold up for travel?", "The XM5 does not fold at the hinges like the XM4, but it comes with a slim moulded carry case."),
            ("Is there a quick charge feature?", "Yes, 3 minutes of charging gives you around 3 hours of playback."),
        ],
        "variants": ["Black", "Silver", "Midnight Blue"],
    },
    {
        "name": "Garmin Forerunner 265 GPS Watch", "category": "Sports & Fitness", "price": 46500,
        "specs": [
            ("Does this model have the AMOLED screen?", "Yes, the Forerunner 265 features a bright, vibrant AMOLED touchscreen display."),
            ("How accurate is the GPS in the city?", "It uses Multi-band GNSS technology, providing excellent accuracy even near tall buildings or dense tree cover."),
            ("Can I store music directly on the watch?", "Absolutely, it has 8GB of internal storage so you can download Spotify playlists for phone-free running."),
            ("What is the battery life in smartwatch mode?", "It lasts up to 13 days in smartwatch mode, or up to 20 hours in GPS mode."),
            ("Is it waterproof for swimming?", "Yes, it carries a 5 ATM rating, so pool and open-water swimming are both fine."),
            ("Does it track sleep and HRV?", "It does — overnight HRV status, sleep stages, and a morning readiness score."),
        ],
        "variants": ["Black/Powder Grey", "Whitestone", "Aqua"],
    },
    {
        "name": "Breville Barista Express Espresso Machine", "category": "Home & Kitchen Appliances", "price": 78000,
        "specs": [
            ("Does it have a built-in grinder?", "Yes, it has an integrated precision conical burr grinder with dose control."),
            ("What size is the portafilter?", "It comes with a standard 54mm stainless steel portafilter."),
            ("Can I manually texture milk for latte art?", "Yes, the powerful steam wand allows you to hand-texture microfoam milk perfect for latte art."),
            ("Is it a single or dual boiler?", "It uses a single Thermocoil heating system, meaning you brew espresso and steam milk sequentially, not simultaneously."),
            ("What is the water tank capacity?", "The removable tank holds 2 litres, which is roughly 15-18 double shots."),
            ("How long does it take to heat up?", "About 30 seconds from cold to first shot thanks to the Thermocoil."),
        ],
        "variants": ["Brushed Stainless Steel", "Black Sesame"],
    },
    {
        "name": "Fujifilm X-T30 II Mirrorless Camera", "category": "Audio & Visual Gear", "price": 98000,
        "specs": [
            ("Does this include a kit lens?", "Yes, this package includes the XC 15-45mm OIS PZ lens."),
            ("Does it have in-body image stabilization (IBIS)?", "No, the X-T30 II does not have IBIS. Stabilization relies on OIS-equipped lenses like the one included."),
            ("How many film simulation modes does it have?", "It features 18 classic Fujifilm film simulation modes, including Classic Neg and Eterna."),
            ("Can it shoot 4K video?", "Yes, it records oversampled 4K/30p video with no crop."),
            ("What is the sensor resolution?", "It uses a 26.1MP X-Trans CMOS 4 APS-C sensor."),
            ("Does it have a microphone input?", "Yes, there's a 3.5mm mic jack, and headphone monitoring works via the USB-C adapter."),
        ],
        "variants": ["Silver", "Charcoal Black"],
    },
    {
        "name": "Samsung T7 Shield 2TB Portable SSD", "category": "Computing & Peripherals", "price": 22500,
        "specs": [
            ("Is it rugged and drop-resistant?", "Yes, it has a tough rubberized exterior and can survive drops from up to 3 meters."),
            ("What are the read and write speeds?", "It delivers sequential read/write speeds of up to 1050/1000 MB/s via USB 3.2 Gen 2."),
            ("Can I record Apple ProRes directly to it from an iPhone 15 Pro?", "Yes, it is fully compatible for direct ProRes 4K recording from the iPhone 15 Pro."),
            ("Is it water resistant?", "It has an IP65 rating for water and dust resistance, making it great for outdoor shoots."),
            ("Does it work with both Windows and Mac?", "Yes, it ships exFAT formatted and works on Windows, macOS, and Android out of the box."),
            ("What cables are included?", "You get both USB-C to C and USB-C to A cables in the box."),
        ],
        "variants": ["Black", "Beige", "Blue"],
    },
    {
        "name": "Dyson Purifier Cool TP07", "category": "Home & Kitchen Appliances", "price": 68000,
        "specs": [
            ("Does it cool the room like an AC?", "No, it is a fan and purifier. It circulates purified air but does not have a compressor to lower the room temperature."),
            ("What kind of filters does it use?", "It uses a fully sealed HEPA H13 standard filter that captures 99.97% of particles as small as 0.3 microns."),
            ("Does it connect to WiFi?", "Yes, you can control it and monitor air quality in real-time using the MyDyson app via WiFi."),
            ("How far does it oscillate?", "It features adjustable oscillation up to 350 degrees to project air across the whole room."),
            ("How often do filters need replacing?", "Roughly every 12 months at 12 hours of daily use; the app tracks remaining filter life."),
            ("Is it loud at night?", "There's a dedicated night mode that caps fan speed and dims the display."),
        ],
        "variants": ["White/Silver", "Black/Nickel"],
    },
    {
        "name": "Viofo A129 Pro Duo 4K Dash Cam", "category": "Automotive & Riding Gear", "price": 23500,
        "specs": [
            ("Is the rear camera also 4K?", "No, the front camera records in true 4K (Sony Exmor R), while the rear camera records in 1080p (Sony Starvis)."),
            ("Does it record while parked?", "Yes, but you need to purchase and install the optional HK3 Hardwire Kit to enable buffered parking mode."),
            ("Does it have built-in WiFi to download videos?", "Yes, it features dual-band (2.4GHz & 5GHz) WiFi for fast video transfers to your phone."),
            ("Does it come with an SD card?", "No, the MicroSD card must be purchased separately. We recommend High Endurance cards."),
            ("Is there a GPS logger?", "Yes, the bundled GPS mount stamps speed and location onto the footage."),
            ("How does it handle heat in summer?", "It uses a supercapacitor instead of a battery, which is far more heat-tolerant for Bangladesh summers."),
        ],
        "variants": ["Standard Bundle", "Bundle + HK3 Kit"],
    },
]

# ============================================================
# 2. PHRASE BANKS
# ============================================================
GREETINGS_BUYER = [
    "Hi there, is the {product} available in ready stock?",
    "Hello! I saw your post regarding the {product}. Do you have it?",
    "Hey, I am interested in purchasing the {product}. Is it available?",
    "Good afternoon, I am looking for the {product}. Can you confirm stock?",
    "Hi, I want to buy the {product}. Let me know if it's available.",
    "Hello, is the {product} currently in stock?",
    "Assalamu alaikum. Do you still have the {product}?",
    "Bhai, {product} ta ki ache? Please confirm.",
    "Hi, quick question — {product}, in stock right now?",
    "Hello. Interested in the {product}. Still selling?",
]

GREETINGS_SELLER = [
    "Hello! Yes, the {product} is available in our ready stock.",
    "Hi there! Thanks for reaching out. We do have it available.",
    "Greetings! Yes, we have brand new units in stock.",
    "Hello sir/ma'am. Yes, it's currently available for immediate delivery.",
    "Hi! Absolutely, we have it ready for you.",
    "Walaikum assalam. Yes bhai, {product} is in stock.",
    "Hello! In stock and ready to dispatch today.",
]

SMALLTALK_BUYER = [
    "Thanks for the quick reply, by the way.",
    "Appreciate you responding so fast.",
    "Good to see an active page for once.",
    "Nice, most pages take hours to reply.",
]

SMALLTALK_SELLER = [
    "Of course, we try to reply within a few minutes during business hours.",
    "Happy to help! We're online from 10 AM to 10 PM daily.",
    "Always here for our customers. Ask me anything about the product.",
    "That's our policy — fast replies, no ghosting.",
]

VARIANT_Q_BUYER = [
    "Which colors do you have in stock?",
    "What variants are available right now?",
    "Do you have any color options, or just one?",
    "Is there a choice of colors or finishes?",
]

VARIANT_A_SELLER = [
    "Right now we have these in stock: {variants}.",
    "Available variants are {variants}.",
    "We currently stock {variants}. All at the same price.",
    "You can pick from {variants}.",
]

STOCK_RECHECK_BUYER = [
    "Just double-checking — it's physically in your shop right now, not on order?",
    "Sorry, one more time: is this in hand, or do you have to bring it in?",
    "Is this ready stock or pre-order? I need to be sure.",
]

STOCK_RECHECK_SELLER = [
    "It's physically in our shop, in hand. We can dispatch today.",
    "Ready stock, sir. Not pre-order. It's on our shelf right now.",
    "In hand and ready. You can even come see it at our outlet.",
]

CONDITION_Q_BUYER = [
    "Awesome. Before we proceed, is it completely brand new and factory sealed?",
    "Great. What condition is it in? Is it 100% intact?",
    "Good to know. Can you confirm if this is official brand new stock with warranty?",
    "Perfect. Just confirming, this is a completely sealed, unopened unit right?",
    "Nice. Does it come intact with the original factory seal?",
    "Is this new or refurbished? I only want brand new.",
    "Any chance this is a used or open-box piece?",
]

CONDITION_A_SELLER = [
    "Yes, it is 100% official brand new, factory sealed with all accessories.",
    "Absolutely. It is completely intact, unopened, and comes with a 1-year official warranty.",
    "Yes sir, we only deal in genuine, factory-sealed products. It's completely brand new.",
    "Of course. It's an official global version, sealed box, with full warranty.",
    "Yes, it is guaranteed brand new and sealed. You'll be the first to open it.",
    "Brand new, untouched, seal intact. We don't sell refurbished items at all.",
]

WARRANTY_Q_BUYER = [
    "What kind of warranty do I get with this?",
    "Is there any warranty coverage? For how long?",
    "Who handles warranty claims if something goes wrong?",
    "Does the warranty cover manufacturing defects?",
]

WARRANTY_A_SELLER = [
    "You get 1 year of official warranty. Claims are handled through our service desk.",
    "1-year replacement warranty against manufacturing defects, processed at our outlet.",
    "Full 1-year warranty. Just bring the invoice and we handle the rest.",
    "Official 1-year coverage. Physical damage and water damage are excluded, as usual.",
]

PROOF_Q_BUYER = [
    "Can you send me a real photo of the actual unit, not a stock image?",
    "Could you share a picture of the sealed box with today's date?",
    "Do you have a video of the actual product in your shop?",
    "Can I see the invoice or import papers to verify it's official?",
]

PROOF_A_SELLER = [
    "Sure, sending a live photo of the sealed unit from our shelf right now.",
    "Of course — here's a short video of the actual box in our showroom.",
    "Attaching a real photo with our shop card next to it for verification.",
    "Yes, I can share the import invoice. We're a registered importer.",
]

PRICE_Q_BUYER = [
    "Alright. So what is the final price for this?",
    "Okay, that sounds good. How much are you asking for it?",
    "Understood. Could you let me know the current price?",
    "Great. What's your best price for this item?",
    "Thanks. How much does it cost in total?",
    "What's the rate on this one?",
    "Price koto? Please let me know.",
]

PRICE_A_SELLER = [
    "The current official price is {price} BDT.",
    "Our selling price for this unit is {price} BDT.",
    "The item is priced at {price} BDT.",
    "For the genuine sealed unit, the price is {price} BDT.",
    "We are currently offering it for {price} BDT.",
    "It's {price} BDT, all inclusive.",
]

DISCOUNT_Q_BUYER = [
    "That's a bit steep. Can you offer any discount on that?",
    "Any chance you can lower the price a bit? Maybe {discount_price} BDT?",
    "I've seen it slightly cheaper elsewhere. Can you do {discount_price} BDT?",
    "Could you give a small discount? My budget is closer to {discount_price} BDT.",
    "Is the price fixed or negotiable? I was hoping for {discount_price} BDT.",
    "Bhai, last koto? {discount_price} BDT hoile nibo.",
    "Can you do anything better? {discount_price} BDT and I'll confirm right now.",
]

DISCOUNT_REJECT_SELLER = [
    "I apologize, but {price} BDT is our final fixed price. Margins on official products are very tight.",
    "Sorry sir, we cannot match that. Our price of {price} BDT is already discounted for genuine stock.",
    "Unfortunately, the price is fixed at {price} BDT. We guarantee the authenticity and warranty, which cheaper stores might compromise on.",
    "We really can't go that low. The best we can do is the stated {price} BDT. It's a premium item.",
    "That's below our cost, honestly. {price} BDT is firm.",
]

DISCOUNT_ACCEPT_SELLER = [
    "Since you are confirming today, I can meet you in the middle at {middle_price} BDT.",
    "I can't do {discount_price}, but as a special offer for a quick deal, I can offer {middle_price} BDT.",
    "Margin is tight, but I want to make this sale. I'll agree to {middle_price} BDT.",
    "Alright, I can give a small concession. Final price {middle_price} BDT. Deal?",
    "For you, {middle_price} BDT. That's genuinely the floor.",
]

SECOND_ROUND_BUYER = [
    "Can you shave off a little more? Round it to {second_price} BDT and I'll confirm now.",
    "Almost there. Do {second_price} BDT and it's a deal.",
    "Meet me at {second_price} BDT and I'll pay immediately.",
]

SECOND_ROUND_SELLER = [
    "That's really the limit — but fine, {second_price} BDT since you're ordering today.",
    "You drive a hard bargain. {second_price} BDT, final.",
    "Okay, {second_price} BDT. But that's absolutely the last adjustment.",
]

BULK_Q_BUYER = [
    "If I take 3 units, can you give a better per-unit rate?",
    "I need multiple pieces for my office. Any bulk pricing?",
    "What if I order 5 of these? Does the price change?",
]

BULK_A_SELLER = [
    "For 3 or more units we can discuss a corporate rate. Please share your requirement in detail.",
    "Yes, bulk orders get a better rate. For 5+ units we offer meaningful savings.",
    "We do offer bulk pricing for offices. Let me know the exact quantity.",
]

COMPARE_Q_BUYER = [
    "How does this compare to the model one tier below it?",
    "Is this worth it over the previous generation?",
    "Another shop is offering a similar item cheaper. Why should I buy from you?",
    "What makes your listing different from the ones on Daraz?",
]

COMPARE_A_SELLER = [
    "The main gains are in build quality and the warranty backing. Cheaper listings are often grey-market imports with no local service.",
    "It's a genuine step up, and more importantly ours is official stock with real warranty support.",
    "We're an authorized reseller with a physical outlet. If anything fails, you have somewhere to go.",
    "Price differences usually come from unofficial imports. Ours is official, with paperwork.",
]

DELIVERY_Q_BUYER = [
    "Okay, how does the delivery process work?",
    "What are the delivery options and charges?",
    "How fast can you deliver it to my address?",
    "I need it delivered to my home. What's the procedure?",
    "Alright. Do you do home delivery? And what is the fee?",
    "Do you deliver outside Dhaka?",
]

DELIVERY_A_SELLER = [
    "We offer home delivery all over Bangladesh via Steadfast/Pathao. Inside Dhaka is 100 BDT (24 hours), Outside Dhaka is 160 BDT (48-72 hours).",
    "Delivery is 100 BDT inside Dhaka and 160 BDT outside. We dispatch immediately upon order confirmation.",
    "We use premium courier services. It takes 1 day for Dhaka (100 BDT) and 2-3 days outside (160 BDT).",
    "Delivery charge is 100 BDT for Dhaka, 160 BDT outside. Packages are fully insured.",
]

URGENT_Q_BUYER = [
    "I need this before tomorrow evening. Is that possible?",
    "Can you do same-day delivery? It's a gift and I'm running out of time.",
    "How soon can it reach me? I need it urgently.",
]

URGENT_A_SELLER = [
    "If you confirm within the next hour, we can dispatch today for next-day delivery inside Dhaka.",
    "Same-day is possible inside Dhaka via Pathao, but the charge would be higher, around 200 BDT.",
    "We can prioritize your parcel. Confirm now and it goes out with today's pickup.",
]

ADVANCE_POLICY_SELLER = [
    "To confirm the order, we require a small 500 BDT advance via bKash to cover the courier booking fee. The rest is Cash on Delivery.",
    "We just need 500 BDT sent to our merchant bKash as a security deposit for the courier. The remaining amount will be collected as COD.",
    "Since it's a high-value item, our policy requires a 500 BDT advance payment. You can pay the rest to the delivery man.",
    "For order confirmation, a 500 BDT advance via bKash is mandatory. The balance is full Cash on Delivery (COD).",
]

ADVANCE_DOUBT_BUYER = [
    "I am not comfortable sending an advance. I've had bad experiences with pages taking advance and blocking. Can you do full COD?",
    "Why the advance? I want 100% Cash on Delivery without any prior payment.",
    "I prefer paying everything when I have the product in my hands. Can we skip the advance?",
    "Is the advance strictly necessary? I'd rather do full COD.",
    "Too many scam pages these days. Why should I trust you with an advance?",
]

ADVANCE_REASSURE_SELLER = [
    "I completely understand your concern. The advance simply ensures you are a serious buyer and covers our return shipping risk if the parcel is rejected. You can check our page reviews and physical shop address for peace of mind.",
    "We sympathize, but this is a strict company policy for items over 10,000 BDT to prevent fake orders. You can verify our trade license and physical store in Multiplan Center.",
    "Sir, it's just 500 BDT for courier security. We have a solid 5-year track record and thousands of reviews. We cannot bypass this policy, unfortunately.",
    "It is standard procedure to avoid fake courier requests. We offer an open-box inspection in front of the rider before you pay the remaining COD amount.",
]

ADVANCE_WAIVE_SELLER = [
    "Alright, for you we'll waive the advance this once. Full COD, but please receive the parcel — rejections cost us.",
    "Okay, since you're local and reachable by phone, we'll do full COD this time.",
    "Fine, we can make an exception. Full Cash on Delivery, no advance needed.",
]

AGREE_TO_ADVANCE_BUYER = [
    "Alright, that makes sense. I will send the 500 BDT advance.",
    "Okay, I understand. I'll trust your page this time. Sending the advance now.",
    "Fair enough. I'll send the 500 BDT to confirm the booking.",
    "Sure, I'll pay the advance. Please share your bKash number.",
]

EXPLICIT_REJECT_BUYER = [
    "No, I won't pay a single taka in advance. If you can't do full COD, then cancel my order.",
    "Sorry, I don't trust Facebook pages with advance payments. I'll buy from a physical shop. Cancel it.",
    "That doesn't work for me. I refuse to pay the advance. Forget it.",
    "Never mind then. If there's no full COD, I am not interested.",
]

# Outcome-specific exits, keyed by the phase where the buyer walks.
DEFER_EXITS = {
    "after_specs": [
        "Thanks for walking me through the specs. I need to sit with this for a day or two before deciding.",
        "This is helpful. Let me think it over and get back to you.",
    ],
    "after_price": [
        "Thanks for all the detailed info. I need to think about it for a bit. I'll let you know.",
        "I appreciate the answers. Let me discuss this with my family and I'll get back to you tomorrow.",
        "Understood. I have to check my budget at the end of the month before committing. I'll message you later.",
    ],
    "after_negotiation": [
        "That's closer, but let me sleep on it. I'll message you if I decide to go ahead.",
        "Appreciate the discount. Still, I want to think it through before confirming.",
    ],
    "after_delivery": [
        "Got it. Let me sort out my schedule for receiving it and I'll confirm later.",
        "Everything sounds fine. I just need a couple of days before I place the order.",
    ],
    "after_advance": [
        "I'll think about the advance policy and let you know. Not saying no, just need a moment.",
        "Let me consider it. I'll message you once I've made up my mind.",
    ],
}

DEFER_SELLER_REPLY = [
    "Sure sir, take your time! We are always here when you are ready.",
    "No rush at all. The offer stands, just message us whenever.",
    "Understood. Feel free to reach out any time — stock changes, though, so don't wait too long.",
    "Of course. We'll keep your preference noted. Talk soon!",
]

# --- Shared closing lines -------------------------------------------------
# Deliberately AMBIGUOUS merchant sign-offs, drawn by MULTIPLE outcomes. In
# v1 (and in the first v2 pass) every outcome owned a private closing bank,
# so the final turn alone identified the label with 100% accuracy -- a model
# could skip the conversation and read the last line. These lines are valid
# after a deferral, a dropout, or a polite rejection alike, which is what
# forces a classifier back into the dialogue body to decide.
AMBIGUOUS_SELLER_CLOSE = [
    "Alright, thanks for your time. Do keep us in mind.",
    "No problem at all. We're here if anything changes.",
    "Understood. Feel free to message us any time.",
    "Sure thing. Have a good day!",
    "Okay, noted. Thanks for reaching out to us.",
    "That's completely fine. Wishing you the best.",
    "Thanks for checking with us. Take care.",
    "Alright. Our inbox is always open if you need anything.",
]

# Buyer sign-offs that are ALSO deliberately ambiguous between "I'm walking
# away for good" (dropout) and "I need time" (deferral). Real Facebook-page
# buyers rarely announce which one they mean, and the seed corpus reflects
# that -- these are sampled by both outcomes so the boundary stays genuinely
# textual rather than template-keyed.
AMBIGUOUS_BUYER_CLOSE = [
    "Okay, thanks for the information.",
    "Alright, got it. Thanks.",
    "I see. Thanks for your help.",
    "Okay. I'll let you know.",
    "Right, thanks for explaining everything.",
    "Understood. Thanks for your time.",
]

DROPOUT_EXITS = {
    "after_specs": [
        "I see. Unfortunately that spec doesn't meet my requirements. Thanks anyway.",
        "Ah, that's a dealbreaker for my use case. I'll look at other models. Thanks.",
    ],
    "after_price": [
        "That's well over my budget, unfortunately. I'll have to skip it.",
        "Too expensive for me right now. Thanks for your time though.",
    ],
    "after_negotiation": [
        "That's too high for me. I'll have to pass and buy from Daraz.",
        "We're too far apart on price. I'll keep looking, thanks.",
    ],
    "after_delivery": [
        "The delivery timeline doesn't work for me. I'll source it locally instead.",
        "That's slower than I need. I'll pass, thanks for the details.",
    ],
    "after_compare": [
        "Based on that, I think the other option suits me better. Thanks for your help.",
        "I'll go with the alternative model then. Appreciate the honesty.",
    ],
}

DROPOUT_SELLER_REPLY = [
    "No problem! Let us know if you need anything else.",
    "We understand. We don't compromise on quality or warranty. Have a good day.",
    "Understood, thanks for considering us. Do check back anytime.",
    "That's alright. Best of luck with your search!",
]

REJECT_SELLER_REPLY = [
    "Understood sir. Your order request has been cancelled. Good luck.",
    "Noted. We can't change the policy, so we'll close this here. Take care.",
    "Alright, cancelling the request. Sorry we couldn't work it out.",
]

COMMIT_ACCEPT_BUYER = [
    "Alright, {agreed_price} BDT sounds fair. I'll take it.",
    "Deal at {agreed_price} BDT. Let's proceed.",
    "Okay, I'm happy with {agreed_price} BDT. Book it for me.",
    "{agreed_price} BDT works. Please confirm my order.",
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
    "Shaheb Bazar, Master Para, Rajshahi",
    "Flat 3A, House 7, Road 27, Mohammadpur, Dhaka",
    "Station Road, Gopalganj Sadar, Gopalganj",
    "College Road, Bogra Sadar, Bogura",
]
PHONES = ["01712349911", "01819876543", "01923456789", "01734567890",
          "01687654321", "01711223388", "01822334455", "01611778899"]

# ============================================================
# 3. ARCHETYPES
# ============================================================
# Each archetype biases which optional phases appear. `weight` controls how
# often the archetype is drawn; `phases` lists optional phases with the
# probability each is included for this archetype.
ARCHETYPES = {
    "Skeptic": {
        "weight": 18,
        "phases": {"condition": 0.95, "warranty": 0.7, "proof": 0.85,
                   "stock_recheck": 0.5, "compare": 0.3, "variant": 0.2},
    },
    "LowBaller": {
        "weight": 16,
        "phases": {"condition": 0.4, "compare": 0.5, "bulk": 0.25,
                   "variant": 0.2, "warranty": 0.2},
        "negotiate_rounds": (1, 3),
    },
    "Ghoster": {
        "weight": 16,
        "phases": {"condition": 0.5, "variant": 0.4, "warranty": 0.3,
                   "smalltalk": 0.3, "compare": 0.3},
    },
    "Urgent": {
        "weight": 14,
        "phases": {"urgent": 0.9, "condition": 0.4, "variant": 0.3,
                   "stock_recheck": 0.4},
    },
    "TechSpecsNerd": {
        "weight": 12,
        "phases": {"condition": 0.4, "compare": 0.5, "warranty": 0.4,
                   "variant": 0.3},
        "spec_range": (3, 5),
    },
    "DeliveryObsessed": {
        "weight": 8,
        "phases": {"urgent": 0.5, "condition": 0.3, "stock_recheck": 0.4},
    },
    "TrustSeeker": {
        "weight": 8,
        "phases": {"proof": 0.9, "warranty": 0.8, "condition": 0.8,
                   "stock_recheck": 0.5},
    },
    "BulkBuyer": {
        "weight": 5,
        "phases": {"bulk": 0.95, "condition": 0.4, "warranty": 0.5,
                   "compare": 0.3},
    },
    "Comparator": {
        "weight": 5,
        "phases": {"compare": 0.95, "condition": 0.4, "warranty": 0.4,
                   "variant": 0.3},
    },
    "Standard": {
        "weight": 8,
        "phases": {"condition": 0.5, "variant": 0.3, "warranty": 0.3,
                   "smalltalk": 0.2, "compare": 0.2},
    },
}

ARCHETYPE_NAMES = list(ARCHETYPES)
ARCHETYPE_WEIGHTS = [ARCHETYPES[a]["weight"] for a in ARCHETYPE_NAMES]


# ============================================================
# 4. DIALOGUE BUILDER
# ============================================================
class DialogueBuilder:
    """Accumulates turns and tracks where the dialogue can legally exit."""

    def __init__(self, rng, product, is_dhaka):
        self.rng = rng
        self.product = product
        self.is_dhaka = is_dhaka
        self.delivery_fee = 100 if is_dhaka else 160
        self.turns = []
        self._tid = 1

    def add(self, role, text, original_intent, normalized_intent):
        """Append a turn, enforcing strict Buyer/Merchant alternation.

        Phases are composed in a randomized order, so two consecutive phases
        can easily both open (or both close) on the same speaker. The 155
        seed dialogues alternate strictly, and the hierarchical classifier
        adds a per-turn role embedding, so a doubled speaker would be an
        out-of-distribution artifact of the generator rather than a property
        of the domain. Merging into the previous turn mirrors how a real
        chat participant sends two thoughts in one message, and keeps the
        turn sequence well-formed no matter what order phases run in.
        """
        if self.turns and self.turns[-1]["role"] == role:
            prev = self.turns[-1]
            prev["text"] = prev["text"].rstrip() + " " + text
            prev["original_intent"] = original_intent
            prev["normalized_intent"] = normalized_intent
            return

        self.turns.append({
            "role": role,
            "text": text,
            "original_intent": original_intent,
            "normalized_intent": normalized_intent,
            "turn_id": self._tid,
        })
        self._tid += 1

    def pick(self, bank, **fmt):
        return self.rng.choice(bank).format(**fmt) if fmt else self.rng.choice(bank)


# --- Individual phases. Each appends turns and returns nothing. ---

def close_soft(b, specific_bank, exit_key, buyer_intent, buyer_norm):
    """Emit a soft (non-purchase) ending.

    With probability `p_ambiguous` the buyer's final line is drawn from the
    SHARED ambiguous bank instead of the outcome-specific one, and the
    merchant's sign-off is shared most of the time. This is what breaks the
    last-turn -> label shortcut; see AMBIGUOUS_SELLER_CLOSE.
    """
    if b.rng.random() < 0.45:
        text = b.pick(AMBIGUOUS_BUYER_CLOSE)
    else:
        text = b.pick(specific_bank[exit_key])
    b.add("Buyer", text, buyer_intent, buyer_norm)

    if b.rng.random() < 0.65:
        b.add("Merchant", b.pick(AMBIGUOUS_SELLER_CLOSE), "ACKNOWLEDGE", "REASSURE_CUSTOMER")
    else:
        bank = DEFER_SELLER_REPLY if specific_bank is DEFER_EXITS else DROPOUT_SELLER_REPLY
        b.add("Merchant", b.pick(bank), "ACKNOWLEDGE", "REASSURE_CUSTOMER")


def phase_greeting(b):
    b.add("Buyer", b.pick(GREETINGS_BUYER, product=b.product["name"]),
          "ASK_AVAILABILITY", "INQUIRE_INFO")
    b.add("Merchant", b.pick(GREETINGS_SELLER, product=b.product["name"]),
          "CONFIRM_AVAILABILITY", "INFORM_PRODUCT")


def phase_smalltalk(b):
    b.add("Buyer", b.pick(SMALLTALK_BUYER), "SMALL_TALK", "INQUIRE_INFO")
    b.add("Merchant", b.pick(SMALLTALK_SELLER), "SMALL_TALK", "INFORM_PRODUCT")


def phase_variant(b):
    b.add("Buyer", b.pick(VARIANT_Q_BUYER), "ASK_VARIANTS", "INQUIRE_INFO")
    b.add("Merchant", b.pick(VARIANT_A_SELLER,
                             variants=", ".join(b.product["variants"])),
          "INFORM_VARIANTS", "INFORM_PRODUCT")


def phase_stock_recheck(b):
    b.add("Buyer", b.pick(STOCK_RECHECK_BUYER), "CHECK_AVAILABILITY", "EXPRESS_DOUBT")
    b.add("Merchant", b.pick(STOCK_RECHECK_SELLER), "CONFIRM_AVAILABILITY", "REASSURE_CUSTOMER")


def phase_condition(b):
    b.add("Buyer", b.pick(CONDITION_Q_BUYER), "ASK_AUTHENTICITY", "EXPRESS_DOUBT")
    b.add("Merchant", b.pick(CONDITION_A_SELLER), "CONFIRM_AUTHENTICITY", "REASSURE_CUSTOMER")


def phase_warranty(b):
    b.add("Buyer", b.pick(WARRANTY_Q_BUYER), "ASK_WARRANTY", "INQUIRE_INFO")
    b.add("Merchant", b.pick(WARRANTY_A_SELLER), "PROVIDE_WARRANTY_INFO", "REASSURE_CUSTOMER")


def phase_proof(b):
    b.add("Buyer", b.pick(PROOF_Q_BUYER), "REQUEST_VERIFICATION", "REQUEST_PROOF")
    b.add("Merchant", b.pick(PROOF_A_SELLER), "PROVIDE_VERIFICATION", "PROVIDE_PROOF")


# Lead-ins that wrap a canned spec answer. The factual answer string stays
# byte-identical (it's the product ground truth), but the surrounding
# phrasing varies, which is what drives merchant text reuse down from ~4.9x
# without inventing product claims the knowledge base doesn't support.
ANSWER_LEADINS = [
    "", "", "",
    "Good question. ",
    "Happy to clarify: ",
    "Right, so ",
    "To be precise, ",
    "Let me confirm that for you. ",
    "Checking the spec sheet — ",
]

# Lead-ins that already assert a positive, so they must NOT be prefixed to an
# answer that itself opens with "Yes"/"No" (that produced "Let me check...
# yes. Yes, it has..." and "Absolutely. No, the X-T30 II does not..."). These
# are only used when the answer does not start with its own polarity word.
ANSWER_LEADINS_ASSERTIVE = [
    "Absolutely. ",
    "Certainly. ",
    "Yes — ",
]

ANSWER_TAILS = [
    "", "", "", "",
    " Hope that helps!",
    " Let me know if you need more detail.",
    " Anything else you'd like to know?",
    " That's straight from the official spec sheet.",
]


def _join_prefix(prefix, sentence):
    """Attach a lead-in without breaking capitalization.

    A prefix ending in a comma or dash continues the sentence, so the
    original capital must be lowered ("Also, What is..." -> "Also, what
    is..."). A prefix ending in sentence-final punctuation leaves the
    following capital intact. Acronyms and model names (IBIS, QMK, 4K) are
    left alone -- only a plain capitalized word is lowered.
    """
    if not prefix:
        return sentence
    if prefix.rstrip().endswith((",", "-", "—", ":")):
        first, _, rest = sentence.partition(" ")
        # Don't touch all-caps tokens or anything with internal capitals.
        if first[:1].isupper() and first[1:].islower():
            sentence = first.lower() + (" " + rest if rest else "")
    return prefix + sentence


def phase_specs(b, n_specs):
    specs = b.rng.sample(b.product["specs"], n_specs)
    connectors = ["I had a technical question. ", "Also, ", "Another thing: ",
                  "I see. And ", "One more on the specs. ", "Quick one - ", ""]
    for i, (q, a) in enumerate(specs):
        prefix = "" if i == 0 and b.rng.random() < 0.4 else b.rng.choice(connectors)
        b.add("Buyer", _join_prefix(prefix, q), "ASK_TECH_SPECS", "INQUIRE_INFO")

        # Only use an assertive lead-in when the answer doesn't already open
        # with its own Yes/No, otherwise the polarity doubles up or clashes.
        opens_polarity = a.lstrip().lower().startswith(("yes", "no", "absolutely", "of course"))
        pool = ANSWER_LEADINS if opens_polarity else ANSWER_LEADINS + ANSWER_LEADINS_ASSERTIVE
        answer = _join_prefix(b.rng.choice(pool), a) + b.rng.choice(ANSWER_TAILS)
        b.add("Merchant", answer, "PROVIDE_TECH_SPECS", "INFORM_PRODUCT")


def phase_compare(b):
    b.add("Buyer", b.pick(COMPARE_Q_BUYER), "COMPARE_PRODUCTS", "INQUIRE_INFO")
    b.add("Merchant", b.pick(COMPARE_A_SELLER), "JUSTIFY_VALUE", "REASSURE_CUSTOMER")


def phase_bulk(b):
    b.add("Buyer", b.pick(BULK_Q_BUYER), "INQUIRE_BULK_DISCOUNT", "INQUIRE_PRICE")
    b.add("Merchant", b.pick(BULK_A_SELLER), "INFORM_BULK_PRICING", "INFORM_PRICE")


def phase_price(b):
    b.add("Buyer", b.pick(PRICE_Q_BUYER), "ASK_PRICE", "INQUIRE_PRICE")
    b.add("Merchant", b.pick(PRICE_A_SELLER, price=f"{b.product['price']:,}"),
          "INFORM_PRICE", "INFORM_PRICE")


def phase_urgent(b):
    b.add("Buyer", b.pick(URGENT_Q_BUYER), "URGENT_DELIVERY_REQUEST", "INQUIRE_INFO")
    b.add("Merchant", b.pick(URGENT_A_SELLER), "CONFIRM_DELIVERY_SPEED", "CREATE_URGENCY")


def phase_delivery(b):
    b.add("Buyer", b.pick(DELIVERY_Q_BUYER), "ASK_DELIVERY", "INQUIRE_INFO")
    b.add("Merchant", b.pick(DELIVERY_A_SELLER), "INFORM_DELIVERY", "INFORM_PRICE")


def phase_negotiation(b, rounds, will_concede):
    """Returns the agreed price (or None if the merchant never conceded)."""
    base = b.product["price"]
    drop = b.rng.randint(1000, 3000)
    ask = base - drop
    b.add("Buyer", b.pick(DISCOUNT_Q_BUYER, discount_price=f"{ask:,}"),
          "NEGOTIATE_PRICE", "NEGOTIATE_PRICE")

    if not will_concede:
        b.add("Merchant", b.pick(DISCOUNT_REJECT_SELLER, price=f"{base:,}"),
              "REJECT_DISCOUNT", "COUNTER_OFFER")
        return None

    agreed = base - (drop // 2)
    b.add("Merchant", b.pick(DISCOUNT_ACCEPT_SELLER,
                             discount_price=f"{ask:,}", middle_price=f"{agreed:,}"),
          "COUNTER_OFFER", "COUNTER_OFFER")

    # Each further round must land strictly BELOW the current agreed price
    # and never below the buyer's own opening ask -- otherwise the buyer ends
    # up "negotiating" themselves upward, which happened when the midpoint
    # (base - drop/2) sat above the ask (base - drop) and a fixed step still
    # cleared it. Stop early if there's no room left to concede.
    for _ in range(rounds - 1):
        room = agreed - ask
        if room <= 100:
            break
        step = min(b.rng.choice([200, 300, 500]), room)
        nxt = agreed - step
        b.add("Buyer", b.pick(SECOND_ROUND_BUYER, second_price=f"{nxt:,}"),
              "NEGOTIATE_PRICE", "NEGOTIATE_PRICE")
        b.add("Merchant", b.pick(SECOND_ROUND_SELLER, second_price=f"{nxt:,}"),
              "COUNTER_OFFER", "COUNTER_OFFER")
        agreed = nxt

    return agreed


def phase_advance(b, buyer_objects, merchant_waives):
    # The advance policy is volunteered by the merchant, so this phase opens
    # on a Merchant turn. If the previous phase also ended on one (delivery
    # usually does), appending a second Merchant turn would break strict
    # Buyer/Merchant alternation -- which the 155 seed dialogues never do,
    # and which the hierarchical classifier's per-turn role embedding would
    # see as an out-of-distribution pattern. Merge into the previous turn
    # instead, exactly as a real seller sending two thoughts in one message.
    b.add("Merchant", b.pick(ADVANCE_POLICY_SELLER),
          "INFORM_PAYMENT_POLICY", "INFORM_PRODUCT")
    if not buyer_objects:
        return
    b.add("Buyer", b.pick(ADVANCE_DOUBT_BUYER), "QUESTION_ADVANCE", "EXPRESS_DOUBT")
    if merchant_waives:
        b.add("Merchant", b.pick(ADVANCE_WAIVE_SELLER), "WAIVE_ADVANCE", "REASSURE_CUSTOMER")
    else:
        b.add("Merchant", b.pick(ADVANCE_REASSURE_SELLER), "JUSTIFY_ADVANCE", "REASSURE_CUSTOMER")


def phase_close(b, agreed_price, advance_waived):
    b.add("Buyer", b.pick(AGREE_TO_ADVANCE_BUYER) if not advance_waived
          else "Great, full COD works for me. Let's do it.",
          "CONFIRM_PURCHASE", "COMMIT_PURCHASE")

    bkash = f"017{b.rng.randint(10000000, 99999999)}"
    if not advance_waived:
        b.add("Merchant",
              f"Thank you for understanding! Please send 500 BDT to {bkash} (Merchant) and share the TrxID.",
              "REQUEST_PAYMENT", "CONFIRM_TRANSACTION")
    else:
        b.add("Merchant",
              "Perfect. Please share your full delivery address and mobile number to book the parcel.",
              "REQUEST_ADDRESS", "CONFIRM_TRANSACTION")

    addr = b.rng.choice(ADDRESSES)
    phone = b.rng.choice(PHONES)
    if not advance_waived:
        trx = f"BK{b.rng.randint(10,99)}X{b.rng.randint(100,999)}P"
        b.add("Buyer",
              f"Sent 500 BDT. TrxID is {trx}. Please deliver to: {addr}. Mobile: {phone}.",
              "PROVIDE_PAYMENT_INFO", "COMMIT_PURCHASE")
        due = agreed_price - 500 + b.delivery_fee
        b.add("Merchant",
              f"Payment received and verified. Your order is confirmed. The remaining {due:,} BDT will be collected on delivery.",
              "CONFIRM_ORDER", "CONFIRM_TRANSACTION")
    else:
        b.add("Buyer", f"Address: {addr}. Mobile: {phone}.",
              "PROVIDE_ADDRESS", "COMMIT_PURCHASE")
        due = agreed_price + b.delivery_fee
        b.add("Merchant",
              f"Order confirmed and booked. Full {due:,} BDT is payable to the rider on delivery.",
              "CONFIRM_ORDER", "CONFIRM_TRANSACTION")


# ============================================================
# 5. COMPOSITIONAL GENERATOR
# ============================================================
# Optional phases available before the pricing block, with their builders.
PRE_PRICE_PHASES = {
    "smalltalk": phase_smalltalk,
    "variant": phase_variant,
    "stock_recheck": phase_stock_recheck,
    "condition": phase_condition,
    "warranty": phase_warranty,
    "proof": phase_proof,
    "compare": phase_compare,
    "bulk": phase_bulk,
    "urgent": phase_urgent,
}


def generate_dialogue(rng, outcome):
    product = rng.choice(PRODUCTS)
    is_dhaka = rng.random() < 0.72
    archetype = rng.choices(ARCHETYPE_NAMES, weights=ARCHETYPE_WEIGHTS)[0]
    cfg = ARCHETYPES[archetype]

    b = DialogueBuilder(rng, product, is_dhaka)

    # --- Choose which optional phases appear, per archetype probability ---
    chosen = [name for name, p in cfg["phases"].items() if rng.random() < p]

    # --- Number of spec questions, decoupled from outcome ---
    lo, hi = cfg.get("spec_range", (1, 4))
    n_specs = rng.randint(lo, min(hi, len(product["specs"])))

    # --- Decide the exit point FIRST, so length can't encode the label ---
    # Each outcome has several legal exit phases; filler phases are added
    # independently of which exit was drawn.
    phase_greeting(b)

    # Order: shuffle the pre-price phases, and let price float among them.
    pre = [PRE_PRICE_PHASES[n] for n in chosen]
    rng.shuffle(pre)

    # "specs" is a block that can land anywhere in the pre-price sequence.
    insert_specs_at = rng.randint(0, len(pre))
    # Price-first buyers ask price before the discovery phases.
    price_first = rng.random() < 0.28

    def run_pre_block(upto=None):
        seq = pre if upto is None else pre[:upto]
        for i, fn in enumerate(seq):
            if i == insert_specs_at and n_specs:
                phase_specs(b, n_specs)
            fn(b)
        if insert_specs_at >= len(seq) and n_specs and upto is None:
            phase_specs(b, n_specs)

    # ---------------- INQUIRY_DROPOUT ----------------
    if outcome == "INQUIRY_DROPOUT":
        exit_at = rng.choice(["after_specs", "after_price", "after_negotiation",
                              "after_delivery", "after_compare"])
        if exit_at == "after_specs":
            cut = rng.randint(0, len(pre))
            run_pre_block(upto=cut)
            phase_specs(b, n_specs)
            close_soft(b, DROPOUT_EXITS, "after_specs", "TERMINATE", "INQUIRE_INFO")
            return b.turns, "no", outcome, "Buyer dropped out early due to technical specification mismatch.", archetype

        if exit_at == "after_compare":
            run_pre_block()
            phase_compare(b)
            close_soft(b, DROPOUT_EXITS, "after_compare", "TERMINATE", "INQUIRE_INFO")
            return b.turns, "no", outcome, "Buyer chose a competing option after a direct comparison.", archetype

        run_pre_block()
        phase_price(b)
        if exit_at == "after_price":
            close_soft(b, DROPOUT_EXITS, "after_price", "TERMINATE", "INQUIRE_PRICE")
            return b.turns, "no", outcome, "Buyer abandoned the inquiry once the price exceeded their budget.", archetype

        if exit_at == "after_delivery":
            phase_delivery(b)
            close_soft(b, DROPOUT_EXITS, "after_delivery", "TERMINATE", "INQUIRE_INFO")
            return b.turns, "no", outcome, "Buyer abandoned the dialogue over unacceptable delivery timelines.", archetype

        phase_negotiation(b, 1, will_concede=False)
        close_soft(b, DROPOUT_EXITS, "after_negotiation", "TERMINATE", "NEGOTIATE_PRICE")
        return b.turns, "no", outcome, "Buyer abandoned dialogue after merchant refused discount.", archetype

    # ---------------- DEFERRED_CONSIDERATION ----------------
    if outcome == "DEFERRED_CONSIDERATION":
        exit_at = rng.choice(["after_specs", "after_price", "after_price",
                              "after_negotiation", "after_delivery", "after_advance"])
        if exit_at == "after_specs":
            cut = rng.randint(0, len(pre))
            run_pre_block(upto=cut)
            phase_specs(b, n_specs)
            close_soft(b, DEFER_EXITS, "after_specs", "DELAY_DECISION", "DEFER_DECISION")
            return b.turns, "no", outcome, "Buyer deferred the decision after reviewing specifications.", archetype

        if price_first:
            phase_price(b)
            run_pre_block()
        else:
            run_pre_block()
            phase_price(b)

        if exit_at == "after_price":
            close_soft(b, DEFER_EXITS, "after_price", "DELAY_DECISION", "DEFER_DECISION")
            return b.turns, "no", outcome, "Buyer deferred decision after learning the price and specs.", archetype

        rounds = rng.randint(1, 2)
        phase_negotiation(b, rounds, will_concede=True)
        if exit_at == "after_negotiation":
            close_soft(b, DEFER_EXITS, "after_negotiation", "DELAY_DECISION", "DEFER_DECISION")
            return b.turns, "no", outcome, "Buyer deferred the decision even after a negotiated discount.", archetype

        phase_delivery(b)
        if exit_at == "after_delivery":
            close_soft(b, DEFER_EXITS, "after_delivery", "DELAY_DECISION", "DEFER_DECISION")
            return b.turns, "no", outcome, "Buyer deferred the decision after reviewing delivery arrangements.", archetype

        phase_advance(b, buyer_objects=rng.random() < 0.6, merchant_waives=False)
        close_soft(b, DEFER_EXITS, "after_advance", "DELAY_DECISION", "DEFER_DECISION")
        return b.turns, "no", outcome, "Buyer deferred the decision pending the advance payment requirement.", archetype

    # ---------------- EXPLICIT_REJECTION ----------------
    if outcome == "EXPLICIT_REJECTION":
        if price_first:
            phase_price(b)
            run_pre_block()
        else:
            run_pre_block()
            phase_price(b)

        if rng.random() < 0.6:
            phase_negotiation(b, rng.randint(1, 2), will_concede=True)
        phase_delivery(b)
        phase_advance(b, buyer_objects=True, merchant_waives=False)
        b.add("Buyer", b.pick(EXPLICIT_REJECT_BUYER), "TERMINATE", "EXPLICIT_REJECTION")
        b.add("Merchant", b.pick(REJECT_SELLER_REPLY), "CANCEL_ORDER", "CONFIRM_TRANSACTION")
        return b.turns, "no", outcome, "Buyer explicitly rejected mandatory advance fee and walked away.", archetype

    # ---------------- PURCHASE_COMMITTED ----------------
    # DECISIVE BUYERS: a real ready-to-buy customer often skips discovery
    # entirely -- greeting, price, done. Without this branch every committed
    # purchase ran the full pre-price block and bottomed out at 15 turns,
    # while dropouts capped at 24, leaving length partially diagnostic. This
    # pushes short commits down into dropout/deferral territory so the
    # turn_count spans genuinely overlap.
    decisive = rng.random() < 0.22
    if decisive:
        # Keep at most one discovery phase, if any.
        pre = pre[:1] if pre and rng.random() < 0.6 else []
        n_specs = rng.randint(0, 1)

    if price_first:
        phase_price(b)
        run_pre_block()
    else:
        run_pre_block()
        phase_price(b)

    agreed = product["price"]
    if rng.random() < (0.25 if decisive else 0.72):
        lo_r, hi_r = cfg.get("negotiate_rounds", (1, 2))
        got = phase_negotiation(b, rng.randint(lo_r, hi_r), will_concede=True)
        if got:
            agreed = got
        b.add("Buyer", b.pick(COMMIT_ACCEPT_BUYER, agreed_price=f"{agreed:,}"),
              "ACCEPT_PRICE", "ACCEPT_OFFER")

    if not decisive or rng.random() < 0.7:
        phase_delivery(b)
    waives = rng.random() < 0.18
    # Decisive buyers usually accept the advance policy without objecting.
    phase_advance(b,
                  buyer_objects=rng.random() < (0.2 if decisive else 0.65),
                  merchant_waives=waives)
    phase_close(b, agreed, advance_waived=waives)

    reason = ("Buyer completed negotiation, accepted advance policy, and committed to purchase."
              if not waives else
              "Buyer committed to purchase after the merchant waived the advance and agreed to full COD.")
    return b.turns, "yes", "PURCHASE_COMMITTED", reason, archetype


# ============================================================
# 6. MAIN
# ============================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=345)
    ap.add_argument("--seed", type=int, default=104)
    args = ap.parse_args()

    with open(SEED_FILE, "r", encoding="utf-8") as f:
        corpus = json.load(f)
    print(f"Loaded {len(corpus)} seed dialogues from generic_dataset.json")

    # Outcome mix, scaled to the requested n.
    mix = {"PURCHASE_COMMITTED": 165, "DEFERRED_CONSIDERATION": 95,
           "INQUIRY_DROPOUT": 75, "EXPLICIT_REJECTION": 10}
    total = sum(mix.values())
    planned = []
    for k, v in mix.items():
        planned += [k] * round(v * args.n / total)
    planned = planned[:args.n]
    while len(planned) < args.n:
        planned.append("PURCHASE_COMMITTED")

    rng = random.Random(args.seed)
    rng.shuffle(planned)

    total_turns = 0
    for i, outcome in enumerate(planned):
        turns, intent, oc, reason, archetype = generate_dialogue(rng, outcome)
        prod_name = None
        for t in turns:
            for p in PRODUCTS:
                if p["name"] in t["text"]:
                    prod_name = p
                    break
            if prod_name:
                break

        corpus.append({
            "dialogue_id": f"ENG_{156 + i:03d}",
            "source_file": "compositional_generator_v2.json",
            "source_model": "compositional-generator-v2",
            "original_id": i + 1,
            "product": prod_name["name"] if prod_name else "Assorted Tech & Gear",
            "category": prod_name["category"] if prod_name else "Mixed",
            "archetype": archetype,
            "language_style": "Pure English",
            "labels": {
                "buying_intent": intent,
                "outcome_category": oc,
                "reason": reason,
            },
            "turn_count": len(turns),
            "turns": turns,
        })
        total_turns += len(turns)

    print(f"Generated {len(planned)} compositional dialogues "
          f"(avg {total_turns/len(planned):.1f} turns).")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        json.dump(corpus, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(corpus)} total dialogues to {TARGET_FILE}")


if __name__ == "__main__":
    main()
