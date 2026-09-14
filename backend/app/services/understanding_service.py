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
    text = description.lower()
    best_hits = -1
    best_sector = None
    for sector, keywords in SECTOR_KEYWORDS.items():
        hits = sum(1 for kw in keywords if kw in text)
        if hits > best_hits:
            best_hits = hits
            best_sector = sector
    return best_sector if best_hits > 0 else None


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

    def _llm_prompt(self, description: str) -> str:
        return (
            "You are a supportive assistant that helps an Indian small-business owner find the "
            "right government schemes. The owner writes about their business freely - it may be "
            "unorganised, awkward, or partial English. Understand their true intent.\n\n"
            f"Sector options (pick closest): {', '.join(SECTOR_VALUES)}. "
            "You can also pick 'null' if nothing fits.\n\n"
            "Business description (raw user text):\n" + (description or "(empty)") + "\n\n"
            "Return ONLY valid JSON with exactly these keys:\n"
            '{'
            '"sector": "one sector value or null", '
            '"tags": ["up to 5 short topic tags in English like: bakery, catering"], '
            '"summary_en": "1-2 simple sentences explaining, in plain words, what the user means their '
            'business is about and what kind of help they might need", '
            '"summary_hi": "same explanation translated into simple Hinglish/Hindi"'
            '}'
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
        return {
            "sector": sector,
            "tags": tags,
            "summary_en": str(data.get("summary_en") or "").strip(),
            "summary_hi": str(data.get("summary_hi") or "").strip(),
        }

    def fallback_understand(self, description: str) -> dict:
        sector = _detect_sector(description)
        tags = _extract_tags(description)
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
        return {
            "sector": sector,
            "tags": tags,
            "summary_en": summary_en,
            "summary_hi": summary_hi,
        }

    def understand(self, description: str) -> dict:
        if self.gemini_enabled:
            parsed = self._parse_llm(self._call_gemini(self._llm_prompt(description)), description)
            if parsed:
                return {**parsed, "provider": "gemini"}
        if self.anthropic_enabled:
            parsed = self._parse_llm(self._call_anthropic(self._llm_prompt(description)), description)
            if parsed:
                return {**parsed, "provider": "anthropic"}
        return {**self.fallback_understand(description), "provider": "builtin"}


understanding_service = UnderstandingService()