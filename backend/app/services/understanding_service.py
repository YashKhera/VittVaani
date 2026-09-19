import json
import re

from app.config import settings
from app.services.gemini_client import call_gemini_text

SECTOR_VALUES = [
    "food_processing", "agriculture", "handicrafts", "textile", "dairy",
    "electronics", "solar_energy", "tourism", "education", "healthcare",
    "it_services", "construction", "transport", "ecommerce",
]

SECTOR_LABELS_EN = {
    "food_processing": "food processing",
    "agriculture": "agriculture & allied",
    "handicrafts": "handicrafts & handloom",
    "textile": "textiles & apparel",
    "dairy": "dairy & livestock",
    "electronics": "electronics & hardware",
    "solar_energy": "solar & renewable energy",
    "tourism": "tourism & hospitality",
    "education": "education & training",
    "healthcare": "healthcare & wellness",
    "it_services": "IT & digital services",
    "construction": "construction & real estate",
    "transport": "transport & logistics",
    "ecommerce": "e-commerce & retail",
}

SECTOR_LABELS_HI = {
    "food_processing": "खाद्य प्रसंस्करण",
    "agriculture": "कृषि एवं संबद्ध",
    "handicrafts": "हस्तशिल्प और हथकरघा",
    "textile": "वस्त्र और परिधान",
    "dairy": "डेयरी और पशुपालन",
    "electronics": "इलेक्ट्रॉनिक्स और हार्डवेयर",
    "solar_energy": "सौर और नवीकरणीय ऊर्जा",
    "tourism": "पर्यटन और आतिथ्य",
    "education": "शिक्षा और प्रशिक्षण",
    "healthcare": "स्वास्थ्य और कल्याण",
    "it_services": "IT और डिजिटल सेवाएँ",
    "construction": "निर्माण और रियल एस्टेट",
    "transport": "परिवहन और लॉजिस्टिक्स",
    "ecommerce": "ई-कॉमर्स और रिटेल",
}

SECTOR_KEYWORDS = {
    "food_processing": ["food", "bakery", "catering", "cooking", "snacks", "namkeen",
                        "pickle", "juice", "spices", "flour", "restaurant", "tiffin",
                        "kitchen", "biscuit", "papad", "masala", "beverage", "achar"],
    "agriculture": ["farm", "farming", "agriculture", "crop", "vegetable", "organic",
                    "horticulture", "poultry", "agri", "seed", "fertilizer"],
    "handicrafts": ["handicraft", "handloom", "pottery", "embroidery", "weave", "artisan",
                    "paint", "crafts", "clay", "jewellery", "jewel", "mat", "basket"],
    "textile": ["textile", "apparel", "garment", "stitch", "tailor", "fabric", "clothing",
                "saree", "sari", "boutique", "dyeing", "knit", "woven", "cloth"],
    "dairy": ["dairy", "milk", "ghee", "paneer", "livestock", "goat", "cow", "cheese",
              "buffalo", "poultry farm"],
    "electronics": ["electronics", "hardware", "electrical", "mobile repair", "appliance",
                    "repair", "cctv", "led", "electronic"],
    "solar_energy": ["solar", "renewable", "energy", "panel", "inverter", "battery", "sun"],
    "tourism": ["tourism", "hotel", "homestay", "hospitality", "travel", "guest house",
                "resort", "tour", "cafe"],
    "education": ["education", "tuition", "coaching", "training", "school", "study",
                  "teaching", "classes", "tutorial", "skill"],
    "healthcare": ["healthcare", "clinic", "pharmacy", "medical", "ayurveda", "doctor",
                   "nursing", "medicine", "physio", "lab"],
    "it_services": ["software", "it services", "app", "website", "digital", "coding",
                    "computer", "web", "mobile app", "cyber", "data"],
    "construction": ["construction", "building", "interior", "civil", "contractor",
                     "real estate", "paint", "plywood", "furniture", "renovation"],
    "transport": ["transport", "logistics", "truck", "taxi", "cab", "delivery",
                  "fleet", "goods", "courier", "van"],
    "ecommerce": ["ecommerce", "e-commerce", "online store", "retail", "shop",
                  "marketplace", "store", "shopping", "seller", "wholesale"],
}

STAGE_VALUES = ["new", "existing"]
SUPPORT_NEED_VALUES = ["capital", "subsidy", "training", "marketing", "legal", "tech"]

PROJECT_TYPE_VALUES = ["business", "education"]

# "education" = the owner (or their family) is pursuing studies and needs
# finance for it. Any description without clear study intent defaults to
# business — that includes people who run/plan teaching & coaching centres.
PROJECT_TYPE_STRONG_EDUCATION = [
    "loan to study", "study loan", "to study", "studying", "for my study",
    "for my studies", "further study", "further studies", "higher education",
    "my education", "education for", "college", "university", "degree",
    "admission", "exam", "upsc", "neet", "jee", "mbbs", "nursing course",
    "bsc", "masters", "postgraduate", "phd", "school fees", "college fees",
    "course fees", "padhai", "parhai", "study karna", "study karni",
]
PROJECT_TYPE_EDUCATION_KEYWORDS = (
    PROJECT_TYPE_STRONG_EDUCATION
    + ["study", "education", "fees for", "student", "diploma"]
)
PROJECT_TYPE_BUSINESS_KEYWORDS = [
    "i run", "i am running", "coaching", "tuition", "classes", "teaching",
    "i teach", "institute", "academy", "training for", "my school",
    "our school", "centre", "center", "training centre", "coaching centre",
    "tuition centre", "i sell", "i make", "my shop",
]

STAGE_LABELS_EN = {"new": "business is just starting", "existing": "business is already running"}
STAGE_LABELS_HI = {"new": "व्यवसाय अभी शुरू हो रहा है", "existing": "व्यवसाय पहले से चल रहा है"}

SUPPORT_NEED_LABELS_EN = {
    "capital": "loan / startup capital",
    "subsidy": "subsidy / grant",
    "training": "training & skill upskilling",
    "marketing": "marketing & market access",
    "legal": "registration & compliance",
    "tech": "technology & digitization",
}

SUPPORT_NEED_LABELS_HI = {
    "capital": "ऋण / स्टार्टअप पूँजी",
    "subsidy": "सब्सिडी / अनुदान",
    "training": "प्रशिक्षण और कौशल",
    "marketing": "मार्केटिंग और बाज़ार",
    "legal": "पंजीकरण और अनुपालन",
    "tech": "तकनीक और डिजिटलीकरण",
}

STAGE_LABEL_TO_VALUE = {
    **{v: k for k, v in STAGE_LABELS_EN.items()},
    **{v: k for k, v in STAGE_LABELS_HI.items()},
}
SUPPORT_NEED_LABEL_TO_VALUE = {
    **{v: k for k, v in SUPPORT_NEED_LABELS_EN.items()},
    **{v: k for k, v in SUPPORT_NEED_LABELS_HI.items()},
}

STAGE_EXISTING_KEYWORDS = [
    "running", "existing", "already", "established", "since", "years", "year",
    "months", "month", "saal", "chal raha", "chala raha", "chal rahi", "chala rahi",
    "operating", "operate", "work done", "2 years", "3 years", "4 years", "5 years",
    "last year", "last 6 months", "doing this", "continue", "also running",
]
STAGE_NEW_KEYWORDS = [
    "start", "startup", "starting", "idea", "planning", "plan to", "planning to",
    "begin", "beginning", "newly", "new", "shuru", "surv kar", "shuru kar",
    "karna chahta", "karna chahti", "want to start", "thinking of", "just started",
    "about to start", "will start", "wish to start", "want start",
    "want to set up", "set up", "open a", "open my", "start my",
]

SUPPORT_NEED_KEYWORDS = {
    "capital": ["loan", "capital", "finance", "fund", "mudra", "udhar", "karz", "finance",
                "paise", "paisa", "money", "cash", "credit", "borrow", "lend", "lihaj"],
    "subsidy": ["subsidy", "grant", "anudan", "sabsidee", "razor", "subvention", "interest subsidy",
                "interest-free", "free"],
    "training": ["training", "skill", "sikh", "course", "workshop", "upskill", "training program",
                 "learn", "classes", "coaching", "mentor"],
    "marketing": ["market", "marketing", "sell", "selling", "buyer", "buyers", "export", "ecommerce",
                  "online sell", "brand", "sales", "customer", "customers", "bazaar", "showroom"],
    "legal": ["registration", "license", "licence", "legal", "gst", "complian", "udyam", "fssai",
              "pan card", "ap-scheme", "certificate", "vendor", "trade"],
    "tech": ["machine", "technology", "digital", "computer", "internet", "equipment", "app",
             "software", "website", "automation", "machinery", "tool", "tools", "solar"],
}

STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "of", "in", "on", "at", "to", "for",
    "with", "from", "by", "my", "our", "your", "is", "are", "was", "were", "am", "be",
    "been", "being", "have", "has", "had", "do", "does", "did", "will", "would", "can",
    "could", "shall", "should", "may", "might", "must", "i", "we", "you", "they", "he",
    "she", "it", "this", "that", "these", "those", "as", "about", "into", "over", "under",
    "again", "then", "once", "here", "there", "all", "any", "each", "some", "no", "not",
    "very", "own", "so", "than", "too", "also", "just", "more", "most", "other", "such",
    "only", "which", "what", "when", "where", "how", "because", "until", "while",
    "business", "businesses", "company", "companies", "shop", "start", "startup",
    "run", "running", "make", "making", "sell", "selling", "small", "day", "days",
    "want", "need", "needs", "help", "helping", "please", "please", "now", "new", "hi",
    "hello", "also", "even", "really", "much", "lot",
}


def _singular(word: str) -> str:
    if len(word) <= 3:
        return word
    if word.endswith("ies"):
        return word[:-3] + "y"
    if word.endswith("ses") and len(word) > 4:
        return word[:-2]
    if word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word


def _extract_tags(description: str, limit: int = 5) -> list[str]:
    if not description:
        return []
    text = description.lower().replace("\n", " ").replace(",", " ").replace("&", " ").replace("-", " ")
    words = text.split()
    seen = set()
    tags = []
    for w in words:
        token = _singular(w.strip(".,;:!?'\"()[]"))
        if len(token) <= 2 or token in STOPWORDS or token in seen:
            continue
        seen.add(token)
        tags.append(token)
        if len(tags) >= limit:
            break
    return tags


def _detect_sector(description: str) -> str | None:
    if not description:
        return None
    text = description.lower().replace("-", " ").replace("_", " ").replace("&", " ")
    text = re.sub(r"[^\w\s]", " ", text)
    words = {_singular(w) for w in text.split()}
    best_hits = 0.0
    best_sector = None
    for sector, keywords in SECTOR_KEYWORDS.items():
        score = 0.0
        for kw in keywords:
            k = kw.lower().replace("-", " ").replace("_", " ")
            if " " in k:
                if k in text:
                    score += 3.0
            elif k in words:
                score += 0.5 + min(len(k), 10) / 10.0
        if score > best_hits:
            best_hits = score
            best_sector = sector
    return best_sector if best_hits > 0 else None


def _detect_stage(description: str) -> str | None:
    if not description:
        return None
    text = description.lower()
    hits = {"existing": 0.0, "new": 0.0}
    for kw in STAGE_EXISTING_KEYWORDS:
        if kw in text:
            hits["existing"] += 2.0 if len(kw.split()) > 1 else 1.0
    for kw in STAGE_NEW_KEYWORDS:
        if kw in text:
            hits["new"] += 2.0 if len(kw.split()) > 1 else 1.0
    if hits["existing"] == hits["new"]:
        return None
    return "existing" if hits["existing"] > hits["new"] else "new"


def _detect_support_needs(description: str) -> list[str]:
    if not description:
        return []
    text = description.lower().replace("-", " ")
    found = []
    for need, keywords in SUPPORT_NEED_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                found.append(need)
                break
    return found


def _detect_stage_safely(description: str) -> str | None:
    return _detect_stage(description)


def _detect_project_type(description: str) -> str | None:
    if not description:
        return None
    text = description.lower()
    edu_hit = any(kw in text for kw in PROJECT_TYPE_EDUCATION_KEYWORDS)
    biz_hit = any(kw in text for kw in PROJECT_TYPE_BUSINESS_KEYWORDS)
    if edu_hit and not biz_hit:
        return "education"
    if edu_hit and biz_hit:
        if any(kw in text for kw in PROJECT_TYPE_STRONG_EDUCATION):
            return "education"
        return "business"
    return "business"


class UnderstandingService:
    def __init__(self):
        self.gemini_enabled = bool(settings.GEMINI_API_KEY)
        self.anthropic_enabled = bool(settings.AI_API_KEY)

    @property
    def provider(self) -> str:
        if self.gemini_enabled:
            return "gemini"
        if self.anthropic_enabled:
            return "anthropic"
        return "builtin"

    def _call_gemini(self, prompt: str, max_tokens: int = 2000) -> str:
        return call_gemini_text(prompt, max_tokens)

    def _call_anthropic(self, prompt: str) -> str:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=settings.AI_API_KEY)
            message = client.messages.create(
                model=settings.AI_MODEL,
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}],
            )
            return message.content[0].text
        except Exception:
            return ""

    def _llm_prompt(self, description: str, language: str = "en") -> str:
        return (
            "You are a supportive assistant that helps an Indian small-business owner find the "
            "right government schemes. The owner writes about their business freely - it may be "
            "unorganised, awkward, or partial English. Understand their true intent.\n\n"
            f"Sector options (pick closest): {', '.join(SECTOR_VALUES)}. "
            "You can also pick 'null' if nothing fits.\n\n"
            f"Stage options (pick closest): {', '.join(STAGE_VALUES)}. "
            "'new' only if the owner says they are starting/planning soon; 'existing' only if the "
            "business is already running. Use 'null' if unclear.\n\n"
            f"Support needs (pick ALL that apply from): {', '.join(SUPPORT_NEED_VALUES)}. "
            "Use an empty array if none are mentioned.\n\n"
            f"project_type (pick one from): {', '.join(PROJECT_TYPE_VALUES)}. "
            "'education' only for someone pursuing their own (or a family member's) studies and "
            "asking for study finance; 'business' for any enterprise the person runs or plans — "
            "including teaching/coaching/tuition centres. Use 'business' if unclear.\n\n"
            "Business description (raw user text):\n" + (description or "(empty)") + "\n\n"
            "Return ONLY valid JSON with exactly these keys:\n"
            '{'
            '"sector": "one sector value or null", '
            '"tags": ["up to 5 short topic tags in English like: bakery, catering"], '
            '"stage": "one stage value or null", '
            '"support_needs": ["all applicable need values or empty array"], '
            '"project_type": "one project_type value", '
            '"summary_en": "1-2 simple sentences explaining, in plain words, what the user means their '
            'business is about and what kind of help they might need", '
            '"summary_hi": "same explanation translated into simple Hinglish/Hindi", '
            + ('"summary_loc": "same explanation in ' + language + ' language, keep it simple and warm"'
                if language not in ("en", "hi") else
                '"summary_loc": ""')
            + '}'
        )

    def _parse_llm(self, raw: str, description: str) -> dict | None:
        if not raw:
            return None
        text = raw.strip()
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.IGNORECASE)
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r"\{[\s\S]*\}", text)
            if not match:
                return None
            try:
                data = json.loads(match.group(0))
            except json.JSONDecodeError:
                return None
        if not isinstance(data, dict):
            return None
        sector = data.get("sector")
        if sector not in SECTOR_VALUES:
            sector = None
        tags = data.get("tags") or []
        if not isinstance(tags, list):
            tags = _extract_tags(description)
        tags = [str(t)[:24] for t in tags[:5]]
        stage = data.get("stage")
        if stage not in STAGE_VALUES:
            stage = None
        needs = data.get("support_needs") or []
        if not isinstance(needs, list):
            needs = _detect_support_needs(description)
        needs = [str(n).strip().lower() for n in needs if str(n).strip().lower() in SUPPORT_NEED_VALUES]
        project_type = data.get("project_type")
        if project_type not in PROJECT_TYPE_VALUES:
            project_type = _detect_project_type(description)
        return {
            "sector": sector,
            "tags": tags,
            "stage": stage,
            "support_needs": needs,
            "project_type": project_type,
            "summary_en": str(data.get("summary_en") or "").strip(),
            "summary_hi": str(data.get("summary_hi") or "").strip(),
            "summary_loc": str(data.get("summary_loc") or "").strip(),
        }

    def fallback_understand(self, description: str, language: str = "en") -> dict:
        sector = _detect_sector(description)
        tags = _extract_tags(description)
        stage = _detect_stage(description)
        needs = _detect_support_needs(description)
        if not description or not description.strip():
            summary_en = "I could not find a description yet. Please type a few lines about your business so I can understand it."
            summary_hi = "मुझे अभी विवरण नहीं मिला। कृपया अपने व्यवसाय के बारे में कुछ पंक्तियाँ लिखें ताकि मैं समझ सकूँ।"
        elif sector:
            label_en = SECTOR_LABELS_EN.get(sector, sector)
            label_hi = SECTOR_LABELS_HI.get(sector, sector)
            summary_en = (
                f"I understand you run a {label_en} business. Your description is mostly about: "
                f"{', '.join(tags) if tags else 'your everyday work'}. "
                "I will look for schemes that fit this kind of work best."
            )
            summary_hi = (
                f"मैं समझ गया — आपका व्यवसाय {label_hi} क्षेत्र में है। आपका विवरण मुख्यतः इन विषयों पर "
                f"केंद्रित है: {', '.join(tags) if tags else 'आपका दैनिक कार्य'}। "
                "मैं ऐसी योजनाएँ खोजूँगा जो इस काम के लिए सबसे उपयुक्त हों।"
            )
        else:
            summary_en = (
                "I couldn't map your business to a specific sector, so I focused on the words you used: "
                f"{', '.join(tags) if tags else 'your key topics'}. "
                "You can tell me more or fix this before moving on."
            )
            summary_hi = (
                "मैं आपके व्यवसाय को किसी विशेष क्षेत्र से नहीं जोड़ पाया, इसलिए मैंने आपके शब्दों पर ध्यान दिया: "
                f"{', '.join(tags) if tags else 'आपके मुख्य विषय'}। "
                "आप और जानकारी दे सकते हैं या इसे ठीक कर सकते हैं।"
            )
        if stage and stage in STAGE_LABELS_EN:
            summary_en += f" Your {STAGE_LABELS_EN[stage]}."
            summary_hi += f" आपका व्यवसाय — {STAGE_LABELS_HI[stage]}।"
        if needs:
            need_labels_en = ", ".join(SUPPORT_NEED_LABELS_EN[n] for n in needs)
            summary_en += f" You seem to need help with: {need_labels_en}."
        return {
            "sector": sector,
            "tags": tags,
            "stage": stage,
            "support_needs": needs,
            "project_type": _detect_project_type(description),
            "summary_en": summary_en,
            "summary_hi": summary_hi,
            "summary_loc": summary_en if language not in ("en", "hi") else "",
        }

    def understand(self, description: str, language: str = "en") -> dict:
        if self.gemini_enabled:
            parsed = self._parse_llm(self._call_gemini(self._llm_prompt(description, language)), description)
            if parsed:
                return {**parsed, "provider": "gemini"}
        if self.anthropic_enabled:
            parsed = self._parse_llm(self._call_anthropic(self._llm_prompt(description, language)), description)
            if parsed:
                return {**parsed, "provider": "anthropic"}
        return {**self.fallback_understand(description, language), "provider": "builtin"}

    def understand_form(self, data: dict, language: str = "en") -> dict:
        """Build an understanding from explicit questionnaire answers.

        The options the user picked are the source of truth. The optional free-text
        description only fills gaps (sector/stage/support needs/project type when the
        user did not pick them) and enriches the summary — it is never required.
        """
        sector = (data.get("sector") or "").strip() or None
        stage_raw = (data.get("stage") or data.get("business_stage") or "").strip() or None
        stage = stage_raw if stage_raw in STAGE_VALUES else STAGE_LABEL_TO_VALUE.get(stage_raw)
        raw_needs = data.get("support_needs") or []
        needs = []
        for n in raw_needs:
            if n in SUPPORT_NEED_VALUES:
                needs.append(n)
            elif n in SUPPORT_NEED_LABEL_TO_VALUE:
                needs.append(SUPPORT_NEED_LABEL_TO_VALUE[n])
        project_type = (data.get("project_type") or "").strip() or None
        description = (data.get("description") or "").strip()

        if sector not in SECTOR_VALUES and sector != "all":
            sector = None
        if stage not in STAGE_VALUES:
            stage = None
        if project_type not in PROJECT_TYPE_VALUES:
            project_type = None
        if not sector:
            sector = _detect_sector(description)
        if not stage:
            stage = _detect_stage(description)
        if not needs:
            needs = _detect_support_needs(description)
        if not project_type:
            project_type = _detect_project_type(description) or "business"

        tags = _extract_tags(description)

        sector_en = SECTOR_LABELS_EN.get(sector, sector.replace("_", " ") if sector else "your venture")
        sector_hi = SECTOR_LABELS_HI.get(sector, sector.replace("_", " ") if sector else "आपका उद्यम")
        stage_en = STAGE_LABELS_EN.get(stage, "")
        stage_hi = STAGE_LABELS_HI.get(stage, "")

        summary_en = f"Your venture is in {sector_en}" if sector else "Your venture profile is saved"
        summary_hi = f"आपका उद्यम {sector_hi} क्षेत्र में है" if sector else "आपकी उद्यम प्रोफ़ाइल सहेजी गई है"
        if stage_en:
            summary_en += f" and your {stage_en}."
            summary_hi += f" — आपका व्यवसाय {stage_hi}।"
        else:
            summary_en += "."
            summary_hi += "।"
        if needs:
            need_en = ", ".join(SUPPORT_NEED_LABELS_EN[n] for n in needs)
            need_hi = ", ".join(SUPPORT_NEED_LABELS_HI.get(n, SUPPORT_NEED_LABELS_EN[n]) for n in needs)
            summary_en += f" You asked for help with: {need_en}."
            summary_hi += f" आपने मदद के लिए चुना: {need_hi}।"
        if description:
            snippet = description.splitlines()[0].strip()[:90]
            summary_en += f" You also told us: “{snippet}”."
            summary_hi += f" आपने यह भी बताया: “{snippet}”।"

        return {
            "sector": sector,
            "tags": tags,
            "stage": stage,
            "support_needs": needs,
            "project_type": project_type,
            "summary_en": summary_en,
            "summary_hi": summary_hi,
            "summary_loc": summary_en if language not in ("en", "hi") else "",
        }


understanding_service = UnderstandingService()