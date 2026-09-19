(function () {
  "use strict";

  window.Questions = {
    sectors: [
      { value: "food_processing", en: "Food processing", hi: "खाद्य प्रसंस्करण" },
      { value: "agriculture", en: "Agriculture & allied", hi: "कृषि एवं संबद्ध" },
      { value: "handicrafts", en: "Handicrafts & handloom", hi: "हस्तशिल्प और हथकरघा" },
      { value: "textile", en: "Textiles & apparel", hi: "वस्त्र और परिधान" },
      { value: "dairy", en: "Dairy & livestock", hi: "डेयरी और पशुपालन" },
      { value: "electronics", en: "Electronics & hardware", hi: "इलेक्ट्रॉनिक्स और हार्डवेयर" },
      { value: "solar_energy", en: "Solar & renewable energy", hi: "सौर और नवीकरणीय ऊर्जा" },
      { value: "tourism", en: "Tourism & hospitality", hi: "पर्यटन और आतिथ्य" },
      { value: "education", en: "Education & training", hi: "शिक्षा और प्रशिक्षण" },
      { value: "healthcare", en: "Healthcare & wellness", hi: "स्वास्थ्य और कल्याण" },
      { value: "it_services", en: "IT & digital services", hi: "IT और डिजिटल सेवाएँ" },
      { value: "construction", en: "Construction & real estate", hi: "निर्माण और रियल एस्टेट" },
      { value: "transport", en: "Transport & logistics", hi: "परिवहन और लॉजिस्टिक्स" },
      { value: "ecommerce", en: "E-commerce & retail", hi: "ई-कॉमर्स और रिटेल" }
    ],

    states: [
      { value: "all", en: "All India", hi: "पूरे भारत" },
      { value: "andhra_pradesh", en: "Andhra Pradesh", hi: "आंध्र प्रदेश" },
      { value: "arunachal_pradesh", en: "Arunachal Pradesh", hi: "अरुणाचल प्रदेश" },
      { value: "assam", en: "Assam", hi: "असम" },
      { value: "bihar", en: "Bihar", hi: "बिहार" },
      { value: "chhattisgarh", en: "Chhattisgarh", hi: "छत्तीसगढ़" },
      { value: "delhi", en: "Delhi", hi: "दिल्ली" },
      { value: "goa", en: "Goa", hi: "गोवा" },
      { value: "gujarat", en: "Gujarat", hi: "गुजरात" },
      { value: "haryana", en: "Haryana", hi: "हरियाणा" },
      { value: "himachal_pradesh", en: "Himachal Pradesh", hi: "हिमाचल प्रदेश" },
      { value: "jharkhand", en: "Jharkhand", hi: "झारखंड" },
      { value: "karnataka", en: "Karnataka", hi: "कर्नाटक" },
      { value: "kerala", en: "Kerala", hi: "केरल" },
      { value: "madhya_pradesh", en: "Madhya Pradesh", hi: "मध्य प्रदेश" },
      { value: "maharashtra", en: "Maharashtra", hi: "महाराष्ट्र" },
      { value: "manipur", en: "Manipur", hi: "मणिपुर" },
      { value: "meghalaya", en: "Meghalaya", hi: "मेघालय" },
      { value: "mizoram", en: "Mizoram", hi: "मिज़ोरम" },
      { value: "nagaland", en: "Nagaland", hi: "नागालैंड" },
      { value: "odisha", en: "Odisha", hi: "ओडिशा" },
      { value: "punjab", en: "Punjab", hi: "पंजाब" },
      { value: "rajasthan", en: "Rajasthan", hi: "राजस्थान" },
      { value: "sikkim", en: "Sikkim", hi: "सिक्किम" },
      { value: "tamil_nadu", en: "Tamil Nadu", hi: "तमिलनाडु" },
      { value: "telangana", en: "Telangana", hi: "तेलंगाना" },
      { value: "tripura", en: "Tripura", hi: "त्रिपुरा" },
      { value: "uttar_pradesh", en: "Uttar Pradesh", hi: "उत्तर प्रदेश" },
      { value: "uttarakhand", en: "Uttarakhand", hi: "उत्तराखंड" },
      { value: "west_bengal", en: "West Bengal", hi: "पश्चिम बंगाल" }
    ],

    stages: [
      { value: "new", en: "Just starting (new)", hi: "अभी शुरू कर रहा/रही हूँ (नया)" },
      { value: "existing", en: "Already running", hi: "पहले से चल रहा है" }
    ],

    revenueGroups: [
      { value: "0_1", en: "Below ₹1 lakh", hi: "₹1 लाख से कम" },
      { value: "1_10", en: "₹1–10 lakh", hi: "₹1–10 लाख" },
      { value: "10l_50l", en: "₹10–50 lakh", hi: "₹10–50 लाख" },
      { value: "50l_plus", en: "Above ₹50 lakh", hi: "₹50 लाख से अधिक" }
    ],

    familyIncomeGroups: [
      { value: "under_2.5l", en: "Below ₹2.5 lakh", hi: "₹2.5 लाख से कम" },
      { value: "2.5l_5l", en: "₹2.5–5 lakh", hi: "₹2.5–5 लाख" },
      { value: "above_5l", en: "Above ₹5 lakh", hi: "₹5 लाख से अधिक" }
    ],

    educationStatuses: [
      { value: "school", en: "SSC / School level", hi: "स्कूल स्तर" },
      { value: "diploma", en: "Diploma", hi: "डिप्लोमा" },
      { value: "undergraduate", en: "Pursuing graduation", hi: "स्नातक कर रहा/रही हूँ" },
      { value: "postgraduate", en: "Pursuing post-graduation", hi: "स्नातकोत्तर कर रहा/रही हूँ" },
      { value: "research", en: "Research / PhD", hi: "शोध / पीएचडी" },
      { value: "not_applicable", en: "Not a student", hi: "छात्र नहीं हूँ" }
    ],

    ageGroups: [
      { value: "18-25", en: "18 – 25", hi: "18 – 25" },
      { value: "26-35", en: "26 – 35", hi: "26 – 35" },
      { value: "36-45", en: "36 – 45", hi: "36 – 45" },
      { value: "46-60", en: "46 – 60", hi: "46 – 60" },
      { value: "60+", en: "60+", hi: "60+" }
    ],

    genders: [
      { value: "female", en: "Female", hi: "महिला" },
      { value: "male", en: "Male", hi: "पुरुष" },
      { value: "other", en: "Other", hi: "अन्य" }
    ],

    entrepreneurTypes: [
      { value: "sc", en: "SC", hi: "अनुसूचित जाति" },
      { value: "st", en: "ST", hi: "अनुसूचित जनजाति" },
      { value: "obc", en: "OBC", hi: "ओबीसी" },
      { value: "pwd", en: "Person with disability", hi: "दिव्यांग" },
      { value: "general", en: "General", hi: "सामान्य" }
    ],

    supportNeeds: {
      financial: [
        { value: "capital", en: "Startup capital / Loan", hi: "स्टार्टअप पूँजी / ऋण" },
        { value: "subsidy", en: "Subsidy / Grant", hi: "सब्सिडी / अनुदान" }
      ],
      nonFinancial: [
        { value: "training", en: "Training & skill upskilling", hi: "प्रशिक्षण और कौशल" },
        { value: "marketing", en: "Marketing & market access", hi: "मार्केटिंग और बाज़ार" },
        { value: "legal", en: "Registration & compliance", hi: "पंजीकरण और अनुपालन" },
        { value: "tech", en: "Technology & digitization", hi: "तकनीक और डिजिटलीकरण" }
      ]
    },

    list: [
      {
        id: "full_name",
        type: "text",
        title: { en: "What is your full name?", hi: "आपका पूरा नाम क्या है?" },
        help: { en: "Your name as shown on your ID / Aadhaar", hi: "आपके आईडी / आधार के अनुसार नाम" }
      },
      {
        id: "phone_number",
        type: "text",
        title: { en: "What is your mobile number?", hi: "आपका मोबाइल नंबर क्या है?" },
        help: { en: "10-digit mobile number", hi: "10 अंकों का मोबाइल नंबर" }
      },
      {
        id: "age_group",
        type: "single",
        title: { en: "What is your age group?", hi: "आपकी आयु किस समूह में है?" },
        options: "ageGroups"
      },
      {
        id: "gender",
        type: "single",
        title: { en: "What is your gender?", hi: "आपका लिंग क्या है?" },
        options: "genders"
      },
      {
        id: "business_sector",
        type: "select",
        title: { en: "What is your business sector?", hi: "आपका व्यवसाय किस क्षेत्र में है?" },
        help: { en: "Choose the closest match.", hi: "सबसे नज़दीकी विकल्प चुनें।" },
        options: "sectors"
      },
      {
        id: "state",
        type: "select",
        title: { en: "Which state do you operate in?", hi: "आप किस राज्य में काम करते हैं?" },
        help: { en: "Many schemes are state-specific.", hi: "कई योजनाएँ राज्य-विशिष्ट हैं।" },
        options: "states"
      },
      {
        id: "business_stage",
        type: "single",
        title: { en: "Is your business running or just starting?", hi: "आपका व्यवसाय चल रहा है या अभी शुरू कर रहे हैं?" },
        options: "stages"
      },
      {
        id: "annual_revenue",
        type: "single",
        title: { en: "What is your estimated annual revenue?", hi: "आपकी अनुमानित वार्षिक आय क्या है?" },
        options: "revenueGroups"
      },
      {
        id: "entrepreneur_type",
        type: "single",
        title: { en: "Do you belong to any of these categories?", hi: "क्या आप इनमें से किसी श्रेणी से आते हैं?" },
        help: { en: "Select all that apply. Helps unlock reserved schemes.", hi: "जो लागू हो चुनें। आरक्षित योजनाओं के लिए ज़रूरी।" },
        options: "entrepreneurTypes"
      },
      {
        id: "annual_family_income",
        type: "single",
        scOnly: true,
        title: { en: "What is your family's annual income?", hi: "आपके परिवार की वार्षिक आय क्या है?" },
        help: { en: "SC concessional loans are for families earning up to ₹5 lakh.", hi: "SC रियायती ऋण ₹5 लाख तक आय वाले परिवारों के लिए हैं।" },
        options: "familyIncomeGroups"
      },
      {
        id: "education_status",
        type: "single",
        scOnly: true,
        title: { en: "What is your education status?", hi: "आपकी शिक्षा की स्थिति क्या है?" },
        help: { en: "Students can access SC education loans.", hi: "छात्र SC शिक्षा ऋण के लिए पात्र हो सकते हैं।" },
        options: "educationStatuses"
      },
      {
        id: "estimated_project_cost",
        type: "num",
        scOnly: true,
        title: { en: "How much will your project cost (₹)?", hi: "आपकी परियोजना की लागत लगभग कितनी है (₹)?" },
        help: { en: "e.g. 150000 — helps pick micro vs term loan size", hi: "जैसे 150000 — माइक्रो बनाम टर्म ऋण चुनने में मदद करता है" }
      },
      {
        id: "financial",
        type: "multi",
        title: { en: "What kind of financial support do you need?", hi: "आपको किस प्रकार की वित्तीय सहायता चाहिए?" },
        options: "financial"
      },
      {
        id: "non_financial",
        type: "multi",
        title: { en: "What other support would help your business grow?", hi: "आपके व्यवसाय को बढ़ाने में और क्या मदद होगी?" },
        options: "nonFinancial"
      },
      {
        id: "description",
        type: "textarea",
        title: { en: "Tell us a little about your business", hi: "अपने व्यवसाय के बारे में हमें बताएँ (वैकल्पिक)" },
        help: { en: "Optional – helps us explain your matches better.", hi: "वैकल्पिक – मैच समझाने में मदद करता है।" }
      },
      {
        id: "understand",
        type: "understand",
        title: { en: "Here is what I understood about your business", hi: "मैंने आपके व्यवसाय के बारे में यह समझा" },
        help: { en: "Based on your answers. Confirm if this is right, so I can match you with the best schemes.", hi: "आपके उत्तरों के आधार पर। सही होने पर पुष्टि करें, ताकि मैं आपको सबसे उपयुक्त योजनाएँ चुन सकूँ।" }
      },
      {
        id: "review",
        type: "review",
        title: { en: "Almost done — review your answers", hi: "अभी बस थोड़ा सा — अपने उत्तर देखें" },
        help: { en: "You can edit any answer by going back.", hi: "आप किसी भी उत्तर को वापस जाकर बदल सकते हैं।" }
      }
    ],

    find: function (id) {
      return this.list.filter(function (q) { return q.id === id; })[0];
    }
  };
})();