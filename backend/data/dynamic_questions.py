"""Curated bank of dynamic follow-up questions.

Each question is filtered by the applicant's:
  - sectors:   only asked for these business sectors (absent = any sector)
  - stages:    only asked for these business stages: "new" | "existing"
               (absent = any stage)
  - education: only asked when education status requires it

Questions are deliberately quick multiple-choice so the flow feels light.
Answers are stored in QuestionnaireProgress and can be used by the
matching engine to refine eligibility/eligibility signals later.
"""

# Single/multi choice helpers keep the phrasing consistent for SC/ST/OBC
# income-sensitive users without asking anything sensitive repeatedly.

DEFAULT_YES_NO = [
    {"value": "yes", "en": "Yes", "hi": "हाँ"},
    {"value": "no", "en": "No", "hi": "नहीं"},
]

COMMON_QUESTIONS = [
    {
        "id": "current_financing",
        "type": "single",
        "stages": ["existing", "expanding"],
        "title": {
            "en": "How is your business financed today?",
            "hi": "आपका व्यवसाय आज कैसे वित्तपोषित है?",
        },
        "help": {
            "en": "This helps us understand your repayment comfort.",
            "hi": "इससे हमें आपकी चुकौती क्षमता समझने में मदद मिलती है।",
        },
        "options": [
            {"value": "self_funded", "en": "Own money / savings", "hi": "अपने पैसे / बचत"},
            {"value": "family_loan", "en": "Family or friends", "hi": "परिवार या मित्र"},
            {"value": "bank_loan", "en": "Bank loan", "hi": "बैंक ऋण"},
            {"value": "microfinance", "en": "Micro-finance / SHG", "hi": "सूक्ष्म-वित्त / स्वयं सहायता समूह"},
            {"value": "other", "en": "Other", "hi": "अन्य"},
        ],
    },
    {
        "id": "monthly_earnings",
        "type": "single",
        "stages": ["existing", "expanding"],
        "title": {
            "en": "What is your average monthly earnings from the business?",
            "hi": "व्यवसाय से आपकी औसत मासिक आय कितनी है?",
        },
        "options": [
            {"value": "below_10k", "en": "Below ₹10,000", "hi": "₹10,000 से कम"},
            {"value": "10k_25k", "en": "₹10,000 – ₹25,000", "hi": "₹10,000 – ₹25,000"},
            {"value": "25k_50k", "en": "₹25,000 – ₹50,000", "hi": "₹25,000 – ₹50,000"},
            {"value": "50k_1l", "en": "₹50,000 – ₹1 lakh", "hi": "₹50,000 – ₹1 लाख"},
            {"value": "above_1l", "en": "Above ₹1 lakh", "hi": "₹1 लाख से अधिक"},
        ],
    },
    {
        "id": "start_capital",
        "type": "single",
        "stages": ["new", "planning"],
        "title": {
            "en": "How much start-up capital do you need?",
            "hi": "आपको कितनी शुरुआती पूँजी चाहिए?",
        },
        "help": {
            "en": "Helps match loans to the right scheme size.",
            "hi": "सही ऋण आकार वाली योजना चुनने में मदद करता है।",
        },
        "options": [
            {"value": "below_50k", "en": "Below ₹50,000", "hi": "₹50,000 से कम"},
            {"value": "50k_1l", "en": "₹50,000 – ₹1 lakh", "hi": "₹50,000 – ₹1 लाख"},
            {"value": "1l_5l", "en": "₹1 – 5 lakh", "hi": "₹1 – 5 लाख"},
            {"value": "5l_10l", "en": "₹5 – 10 lakh", "hi": "₹5 – 10 लाख"},
            {"value": "above_10l", "en": "Above ₹10 lakh", "hi": "₹10 लाख से अधिक"},
        ],
    },
    {
        "id": "existing_loan",
        "type": "single",
        "title": {
            "en": "Are you currently repaying any existing loan?",
            "hi": "क्या आप वर्तमान में कोई चालू ऋण चुका रहे हैं?",
        },
        "options": DEFAULT_YES_NO,
    },
    {
        "id": "collateral",
        "type": "single",
        "title": {
            "en": "If you need a loan, what security can you offer?",
            "hi": "अगर आपको ऋण चाहिए, तो आप क्या ज़मानत दे सकते हैं?",
        },
        "help": {
            "en": "Guarantee-free concessional loans exist — this helps us shortlist them.",
            "hi": "बिना ज़मानत के रियायती ऋण उपलब्ध हैं — इससे हमें सही योजनाएँ छाँटने में मदद मिलती है।",
        },
        "options": [
            {"value": "land", "en": "Land / property", "hi": "ज़मीन / संपत्ति"},
            {"value": "gold", "en": "Gold / jewellery", "hi": "सोना / आभूषण"},
            {"value": "guarantor", "en": "Family guarantor", "hi": "परिवार का ज़मानतदार"},
            {"value": "none", "en": "I cannot offer any", "hi": "मैं कुछ नहीं दे सकता"},
        ],
    },
]

# Conditionally offered when the applicant is a student — directly feeds the
# SC/ST concessional Education Loan schemes.
EDUCATION_QUESTIONS = [
    {
        "id": "ed_loan_needed",
        "type": "single",
        "education_required": True,
        "title": {
            "en": "Are you looking for an education loan to fund your studies?",
            "hi": "क्या आप अपनी पढ़ाई के लिए शिक्षा ऋण चाहते हैं?",
        },
        "help": {
            "en": "SC/ST students can get concessional education loans.",
            "hi": "अनुसूचित जाति/जनजाति के विद्यार्थियों को रियायती शिक्षा ऋण मिलता है।",
        },
        "options": DEFAULT_YES_NO,
    },
    {
        "id": "ed_course_goal",
        "type": "text",
        "education_required": True,
        "title": {
            "en": "Which course or stream do you plan to study?",
            "hi": "आप किस पाठ्यक्रम या विषय में पढ़ाई करना चाहते हैं?",
        },
        "help": {
            "en": "e.g. B.Tech, nursing, ITI, MBA…",
            "hi": "जैसे: बी.टेक, नर्सिंग, आईटीआई, एमबीए…",
        },
    },
    {
        "id": "ed_institution",
        "type": "single",
        "education_required": True,
        "title": {
            "en": "What type of institution will you join?",
            "hi": "आप किस प्रकार की संस्था में जाएंगे?",
        },
        "options": [
            {"value": "government", "en": "Government college", "hi": "सरकारी कॉलेज"},
            {"value": "private", "en": "Private college", "hi": "निजी कॉलेज"},
            {"value": "vocational", "en": "ITI / vocational centre", "hi": "आईटीआई / व्यावसायिक केंद्र"},
            {"value": "coaching", "en": "Coaching / certification", "hi": "कोचिंग / प्रमाणन"},
        ],
    },
]

SECTOR_QUESTIONS = {
    "food_processing": [
        {
            "id": "fp_raw_material",
            "type": "single",
            "title": {
                "en": "Where do you get your raw material from?",
                "hi": "आपका कच्चा माल कहाँ से मिलता है?",
            },
            "options": [
                {"value": "own_farm", "en": "My own farm / field", "hi": "मेरा अपना खेत"},
                {"value": "local_market", "en": "Local market", "hi": "स्थानीय बाज़ार"},
                {"value": "supplier", "en": "Regular supplier", "hi": "नियमित आपूर्तिकर्ता"},
                {"value": "imported", "en": "From another state / import", "hi": "दूसरे राज्य / आयात से"},
            ],
        },
        {
            "id": "fp_capacity",
            "type": "single",
            "title": {
                "en": "How much do you process in a month?",
                "hi": "आप एक महीने में कितना प्रसंस्करण करते हैं?",
            },
            "options": [
                {"value": "below_500kg", "en": "Below 500 kg", "hi": "500 किग्रा से कम"},
                {"value": "500kg_1t", "en": "500 kg – 1 tonne", "hi": "500 किग्रा – 1 टन"},
                {"value": "1t_5t", "en": "1 – 5 tonnes", "hi": "1 – 5 टन"},
                {"value": "above_5t", "en": "Above 5 tonnes", "hi": "5 टन से अधिक"},
            ],
        },
        {
            "id": "fp_cold_storage",
            "type": "single",
            "title": {
                "en": "Do you have cold storage or processing equipment?",
                "hi": "क्या आपके पास कोल्ड स्टोरेज या प्रसंस्करण उपकरण हैं?",
            },
            "options": [
                {"value": "own", "en": "Yes, my own", "hi": "हाँ, अपना"},
                {"value": "rented", "en": "Rented / shared", "hi": "किराए / साझा पर"},
                {"value": "none", "en": "Not yet needed", "hi": "अभी ज़रूरत नहीं"},
            ],
        },
        {
            "id": "fp_certifications",
            "type": "multi",
            "title": {
                "en": "Which of these do you have?",
                "hi": "इनमें से आपके पास क्या है?",
            },
            "options": [
                {"value": "fssai", "en": "FSSAI license", "hi": "FSSAI लाइसेंस"},
                {"value": "gst", "en": "GST registration", "hi": "GST पंजीकरण"},
                {"value": "udyam", "en": "Udyam (MSME)", "hi": "उद्यम (एमएसएमई)"},
                {"value": "export", "en": "Export license", "hi": "निर्यात लाइसेंस"},
                {"value": "none", "en": "None yet", "hi": "अभी कुछ नहीं"},
            ],
        },
    ],
    "agriculture": [
        {
            "id": "ag_land",
            "type": "single",
            "title": {
                "en": "How much land do you cultivate?",
                "hi": "आप कितनी ज़मीन पर खेती करते हैं?",
            },
            "options": [
                {"value": "below_1acre", "en": "Below 1 acre", "hi": "1 एकड़ से कम"},
                {"value": "1_2_acre", "en": "1 – 2 acres", "hi": "1 – 2 एकड़"},
                {"value": "2_5_acre", "en": "2 – 5 acres", "hi": "2 – 5 एकड़"},
                {"value": "above_5acre", "en": "Above 5 acres", "hi": "5 एकड़ से अधिक"},
            ],
        },
        {
            "id": "ag_irrigation",
            "type": "single",
            "title": {
                "en": "What kind of irrigation do you use?",
                "hi": "आप किस प्रकार की सिंचाई करते हैं?",
            },
            "options": [
                {"value": "rainfed", "en": "Rain-fed", "hi": "बारिश पर निर्भर"},
                {"value": "well", "en": "Well / borewell", "hi": "कुआँ / बोरवेल"},
                {"value": "canal", "en": "Canal", "hi": "नहर"},
                {"value": "drip", "en": "Drip / sprinkler", "hi": "ड्रिप / फव्वारा"},
            ],
        },
        {
            "id": "ag_warehouse",
            "type": "single",
            "title": {
                "en": "Do you have your own storage / godown?",
                "hi": "क्या आपके पास अपना भंडारण / गोदाम है?",
            },
            "options": DEFAULT_YES_NO,
        },
        {
            "id": "ag_labour",
            "type": "single",
            "title": {
                "en": "How many workers do you employ during harvest?",
                "hi": "फसल कटाई के समय आप कितने मज़दूर लगाते हैं?",
            },
            "options": [
                {"value": "0_2", "en": "0 – 2", "hi": "0 – 2"},
                {"value": "3_10", "en": "3 – 10", "hi": "3 – 10"},
                {"value": "above_10", "en": "More than 10", "hi": "10 से अधिक"},
            ],
        },
    ],
    "dairy": [
        {
            "id": "dy_herd",
            "type": "single",
            "title": {
                "en": "How many cattle do you have?",
                "hi": "आपके पास कितने पशु हैं?",
            },
            "options": [
                {"value": "1_2", "en": "1 – 2", "hi": "1 – 2"},
                {"value": "3_10", "en": "3 – 10", "hi": "3 – 10"},
                {"value": "11_50", "en": "11 – 50", "hi": "11 – 50"},
                {"value": "above_50", "en": "Above 50", "hi": "50 से अधिक"},
            ],
        },
        {
            "id": "dy_feed",
            "type": "single",
            "title": {
                "en": "How do you manage animal feed?",
                "hi": "आप पशु चारा कैसे प्रबंधित करते हैं?",
            },
            "options": [
                {"value": "own_fodder", "en": "My own fodder", "hi": "अपना चारा"},
                {"value": "partly_buy", "en": "Partly buy from market", "hi": "थोड़ा बाज़ार से खरीदता हूँ"},
                {"value": "fully_buy", "en": "Buy everything", "hi": "पूरा बाज़ार से"},
            ],
        },
        {
            "id": "dy_chiller",
            "type": "single",
            "title": {
                "en": "Do you have a milk chiller or cooling facility?",
                "hi": "क्या आपके पास दूध कूलिंग की सुविधा है?",
            },
            "options": DEFAULT_YES_NO,
        },
    ],
    "handicrafts": [
        {
            "id": "hc_products",
            "type": "multi",
            "title": {
                "en": "What kind of products do you make?",
                "hi": "आप किस तरह की चीज़ें बनाते हैं?",
            },
            "options": [
                {"value": "carpets", "en": "Carpets / rugs", "hi": "कालीन / दरी"},
                {"value": "wood", "en": "Woodwork / furniture", "hi": "लकड़ी का सामान"},
                {"value": "ceramics", "en": "Pottery / ceramics", "hi": "मिट्टी के बर्तन"},
                {"value": "textile_craft", "en": "Handloom / embroidery", "hi": "हथकरघा / कढ़ाई"},
                {"value": "jewellery", "en": "Jewellery / beads", "hi": "आभूषण / मनके"},
                {"value": "other", "en": "Other handcrafts", "hi": "अन्य"},
            ],
        },
        {
            "id": "hc_channels",
            "type": "multi",
            "title": {
                "en": "Where do you currently sell your products?",
                "hi": "आप वर्तमान में अपने उत्पाद कहाँ बेचते हैं?",
            },
            "options": [
                {"value": "local_mela", "en": "Local haat / mela", "hi": "स्थानीय हाट / मेला"},
                {"value": "retail", "en": "Retail / shops", "hi": "दुकानें / रिटेल"},
                {"value": "online", "en": "Online", "hi": "ऑनलाइन"},
                {"value": "export", "en": "Export / bulk orders", "hi": "निर्यात / थोक ऑर्डर"},
            ],
        },
        {
            "id": "hc_rawmat",
            "type": "single",
            "title": {
                "en": "Where does your raw material come from?",
                "hi": "आपका कच्चा माल कहाँ से आता है?",
            },
            "options": [
                {"value": "local", "en": "Local / nearby", "hi": "स्थानीय / आस-पास"},
                {"value": "state", "en": "Within the state", "hi": "राज्य के भीतर"},
                {"value": "import", "en": "Another state / import", "hi": "दूसरे राज्य / आयात"},
            ],
        },
    ],
    "textile": [
        {
            "id": "tx_units",
            "type": "single",
            "title": {
                "en": "How many looms / sewing machines do you run?",
                "hi": "आप कितनी करघे / सिलाई मशीनें चलाते हैं?",
            },
            "options": [
                {"value": "0_2", "en": "0 – 2", "hi": "0 – 2"},
                {"value": "3_10", "en": "3 – 10", "hi": "3 – 10"},
                {"value": "11_50", "en": "11 – 50", "hi": "11 – 50"},
                {"value": "above_50", "en": "More than 50", "hi": "50 से अधिक"},
            ],
        },
        {
            "id": "tx_design",
            "type": "single",
            "title": {
                "en": "Do you design your products in-house?",
                "hi": "क्या आप अपने उत्पादों का डिज़ाइन खुद करते हैं?",
            },
            "options": DEFAULT_YES_NO,
        },
    ],
    "electronics": [
        {
            "id": "el_products",
            "type": "multi",
            "title": {
                "en": "What do you make / assemble?",
                "hi": "आप क्या बनाते / असेंबल करते हैं?",
            },
            "options": [
                {"value": "mobile", "en": "Mobile & accessories", "hi": "मोबाइल और सामान"},
                {"value": "led", "en": "LED / lighting", "hi": "LED / लाइटिंग"},
                {"value": "pcb", "en": "PCBs / components", "hi": "PCB / कंपोनेंट"},
                {"value": "power", "en": "Power supplies / inverters", "hi": "पॉवर सप्लाई / इन्वर्टर"},
                {"value": "repair", "en": "Repair services", "hi": "मरम्मत सेवाएँ"},
            ],
        },
        {
            "id": "el_space",
            "type": "single",
            "title": {
                "en": "Where do you produce?",
                "hi": "आप कहाँ उत्पादन करते हैं?",
            },
            "options": [
                {"value": "own", "en": "Own premises", "hi": "अपना परिसर"},
                {"value": "rented", "en": "Rented premises", "hi": "किराये का परिसर"},
                {"value": "home", "en": "Home-based", "hi": "घर से"},
            ],
        },
    ],
    "solar_energy": [
        {
            "id": "so_services",
            "type": "multi",
            "title": {
                "en": "What do you do in solar?",
                "hi": "सौर ऊर्जा में आप क्या करते हैं?",
            },
            "options": [
                {"value": "installation", "en": "Installation", "hi": "इंस्टॉलेशन"},
                {"value": "assembly", "en": "Panel assembly", "hi": "पैनल असेंबली"},
                {"value": "sales", "en": "Sales / rental", "hi": "बिक्री / किराया"},
                {"value": "maintenance", "en": "Maintenance", "hi": "रखरखाव"},
            ],
        },
        {
            "id": "so_order_size",
            "type": "single",
            "title": {
                "en": "What is your usual project size?",
                "hi": "आपके आम प्रोजेक्ट का आकार क्या है?",
            },
            "options": [
                {"value": "below_50k", "en": "Below ₹50,000", "hi": "₹50,000 से कम"},
                {"value": "50k_2l", "en": "₹50,000 – ₹2 lakh", "hi": "₹50,000 – ₹2 लाख"},
                {"value": "2l_10l", "en": "₹2 – 10 lakh", "hi": "₹2 – 10 लाख"},
                {"value": "above_10l", "en": "Above ₹10 lakh", "hi": "₹10 लाख से अधिक"},
            ],
        },
    ],
    "tourism": [
        {
            "id": "to_type",
            "type": "multi",
            "title": {
                "en": "What kind of tourism business is it?",
                "hi": "यह किस प्रकार का पर्यटन व्यवसाय है?",
            },
            "options": [
                {"value": "homestay", "en": "Homestay / hotel", "hi": "होमस्टे / होटल"},
                {"value": "travel", "en": "Travel agency", "hi": "ट्रैवल एजेंसी"},
                {"value": "guiding", "en": "Tour guiding", "hi": "टूर गाइडिंग"},
                {"value": "cafe", "en": "Café / restaurant", "hi": "कैफ़े / रेस्तराँ"},
                {"value": "souvenir", "en": "Souvenirs & craft shop", "hi": "स्मृति चिन्ह और शिल्प दुकान"},
            ],
        },
        {
            "id": "to_season",
            "type": "single",
            "title": {
                "en": "When is your peak season?",
                "hi": "आपका सबसे व्यस्त सीज़न कब है?",
            },
            "options": [
                {"value": "jan_mar", "en": "Jan – Mar", "hi": "जन – मार्च"},
                {"value": "apr_jun", "en": "Apr – Jun", "hi": "अप्रैल – जून"},
                {"value": "jul_sep", "en": "Jul – Sep", "hi": "जुल – सितं"},
                {"value": "oct_dec", "en": "Oct – Dec", "hi": "अक्टू – दिसं"},
            ],
        },
    ],
    "education": [
        {
            "id": "ed_level",
            "type": "single",
            "title": {
                "en": "What level of course is it?",
                "hi": "यह किस स्तर का पाठ्यक्रम है?",
            },
            "options": [
                {"value": "school", "en": "School level", "hi": "स्कूल स्तर"},
                {"value": "diploma", "en": "Diploma", "hi": "डिप्लोमा"},
                {"value": "undergraduate", "en": "Graduation", "hi": "स्नातक"},
                {"value": "postgraduate", "en": "Post-graduation", "hi": "स्नातकोत्तर"},
                {"value": "vocational", "en": "Vocational / skill", "hi": "व्यावसायिक / कौशल"},
            ],
        },
        {
            "id": "ed_course",
            "type": "text",
            "title": {
                "en": "Which course do you plan to join?",
                "hi": "आप कौन-सा पाठ्यक्रम करना चाहते हैं?",
            },
            "help": {
                "en": "e.g. ITI electrician, B.Com, nursing…",
                "hi": "जैसे: ITI इलेक्ट्रीशियन, B.Com, नर्सिंग…",
            },
        },
        {
            "id": "ed_budget",
            "type": "single",
            "title": {
                "en": "What is your course fee budget per year?",
                "hi": "आपके पाठ्यक्रम की वार्षिक फीस कितनी है?",
            },
            "options": [
                {"value": "below_50k", "en": "Below ₹50,000", "hi": "₹50,000 से कम"},
                {"value": "50k_1l", "en": "₹50,000 – ₹1 lakh", "hi": "₹50,000 – ₹1 लाख"},
                {"value": "1l_3l", "en": "₹1 – 3 lakh", "hi": "₹1 – 3 लाख"},
                {"value": "above_3l", "en": "Above ₹3 lakh", "hi": "₹3 लाख से अधिक"},
            ],
        },
    ],
    "healthcare": [
        {
            "id": "he_type",
            "type": "single",
            "title": {
                "en": "What kind of healthcare business is it?",
                "hi": "यह किस प्रकार का स्वास्थ्य व्यवसाय है?",
            },
            "options": [
                {"value": "clinic", "en": "Clinic", "hi": "क्लिनिक"},
                {"value": "pharmacy", "en": "Pharmacy", "hi": "दवा दुकान"},
                {"value": "wellness", "en": "Wellness / fitness centre", "hi": "वेलनेस / फिटनेस केंद्र"},
                {"value": "telehealth", "en": "Telehealth / lab", "hi": "टेलीहेल्थ / प्रयोगशाला"},
            ],
        },
        {
            "id": "he_space",
            "type": "single",
            "title": {
                "en": "Is your premises owned or rented?",
                "hi": "आपका परिसर अपना है या किराये का?",
            },
            "options": [
                {"value": "own", "en": "Own", "hi": "अपना"},
                {"value": "rented", "en": "Rented", "hi": "किराये का"},
            ],
        },
    ],
    "it_services": [
        {
            "id": "it_services",
            "type": "multi",
            "title": {
                "en": "Which IT services do you offer?",
                "hi": "आप कौन-सी IT सेवाएँ देते हैं?",
            },
            "options": [
                {"value": "web", "en": "Websites", "hi": "वेबसाइट"},
                {"value": "apps", "en": "Mobile apps", "hi": "मोबाइल ऐप"},
                {"value": "digital", "en": "Digital marketing", "hi": "डिजिटल मार्केटिंग"},
                {"value": "software", "en": "Software development", "hi": "सॉफ़्टवेयर विकास"},
                {"value": "support", "en": "IT support / AMC", "hi": "IT सपोर्ट / AMC"},
            ],
        },
        {
            "id": "it_team",
            "type": "single",
            "title": {
                "en": "How big is your team?",
                "hi": "आपकी टीम कितनी बड़ी है?",
            },
            "options": [
                {"value": "solo", "en": "Just me", "hi": "सिर्फ़ मैं"},
                {"value": "2_5", "en": "2 – 5 people", "hi": "2 – 5 लोग"},
                {"value": "above_5", "en": "More than 5", "hi": "5 से अधिक"},
            ],
        },
    ],
    "construction": [
        {
            "id": "co_projects",
            "type": "multi",
            "title": {
                "en": "What kind of construction projects do you take?",
                "hi": "आप किस तरह के निर्माण प्रोजेक्ट लेते हैं?",
            },
            "options": [
                {"value": "housing", "en": "Housing", "hi": "आवासीय"},
                {"value": "commercial", "en": "Commercial", "hi": "वाणिज्यिक"},
                {"value": "roads", "en": "Roads / infra", "hi": "सड़क / बुनियादी"},
                {"value": "interior", "en": "Interior / renovation", "hi": "इंटीरियर / नवीनीकरण"},
            ],
        },
        {
            "id": "co_team",
            "type": "single",
            "title": {
                "en": "How many workers are on your team?",
                "hi": "आपकी टीम में कितने मज़दूर हैं?",
            },
            "options": [
                {"value": "below_5", "en": "Below 5", "hi": "5 से कम"},
                {"value": "5_20", "en": "5 – 20", "hi": "5 – 20"},
                {"value": "above_20", "en": "More than 20", "hi": "20 से अधिक"},
            ],
        },
    ],
    "transport": [
        {
            "id": "tr_fleet",
            "type": "single",
            "title": {
                "en": "How many vehicles does your fleet have?",
                "hi": "आपके बेड़े में कितने वाहन हैं?",
            },
            "options": [
                {"value": "zero", "en": "None yet", "hi": "अभी कोई नहीं"},
                {"value": "1_2", "en": "1 – 2", "hi": "1 – 2"},
                {"value": "3_10", "en": "3 – 10", "hi": "3 – 10"},
                {"value": "above_10", "en": "More than 10", "hi": "10 से अधिक"},
            ],
        },
        {
            "id": "tr_types",
            "type": "multi",
            "title": {
                "en": "What kind of vehicles do you run?",
                "hi": "आप किस प्रकार के वाहन चलाते हैं?",
            },
            "options": [
                {"value": "goods", "en": "Goods truck / tempo", "hi": "माल ट्रक / टेंपो"},
                {"value": "passenger", "en": "Passenger (taxi/bus)", "hi": "यात्री (टैक्सी/बस)"},
                {"value": "erickshaw", "en": "E-rickshaw / 3-wheeler", "hi": "ई-रिक्शा / तिपहिया"},
                {"value": "courier", "en": "Bike / courier", "hi": "बाइक / कूरियर"},
            ],
        },
    ],
    "ecommerce": [
        {
            "id": "ec_platforms",
            "type": "multi",
            "title": {
                "en": "Where do you sell online?",
                "hi": "आप ऑनलाइन कहाँ बेचते हैं?",
            },
            "options": [
                {"value": "amazon", "en": "Amazon", "hi": "अमेज़न"},
                {"value": "flipkart", "en": "Flipkart", "hi": "फ्लिपकार्ट"},
                {"value": "meesho", "en": "Meesho", "hi": "मीशो"},
                {"value": "own", "en": "My own website / app", "hi": "अपनी वेबसाइट / ऐप"},
                {"value": "social", "en": "WhatsApp / Instagram", "hi": "व्हाट्सऐप / इंस्टाग्राम"},
            ],
        },
        {
            "id": "ec_orders",
            "type": "single",
            "title": {
                "en": "How many orders do you get in a month?",
                "hi": "आपको एक महीने में कितने ऑर्डर मिलते हैं?",
            },
            "options": [
                {"value": "below_100", "en": "Below 100", "hi": "100 से कम"},
                {"value": "100_1000", "en": "100 – 1,000", "hi": "100 – 1,000"},
                {"value": "above_1000", "en": "More than 1,000", "hi": "1,000 से अधिक"},
            ],
        },
        {
            "id": "ec_inventory",
            "type": "single",
            "title": {
                "en": "Do you keep your own inventory / warehouse?",
                "hi": "क्या आप अपना इन्वेंटरी / गोदाम रखते हैं?",
            },
            "options": DEFAULT_YES_NO,
        },
    ],
}

# Order in which common and sector questions are offered when no explicit
# ordering matters (sector questions come first, then the common ones).
SECTOR_ORDER = list(SECTOR_QUESTIONS.keys())

ALL_QUESTIONS = list(SECTOR_QUESTIONS.values()) + [COMMON_QUESTIONS]


def all_questions():
    """Flatten every bank question into one list."""
    flat = []
    for group in ALL_QUESTIONS:
        flat.extend(group)
    flat.extend(EDUCATION_QUESTIONS)
    return flat