from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.profile import EntrepreneurProfile
from app.models.scheme import Scheme
from app.utils.constants import FAMILY_INCOME_BANDS, LOAN_CATEGORY_COST_CEILING, MATCH_WEIGHTS
from app.utils.helpers import normalize_list

EDUCATION_PURSUING = {"school", "diploma", "undergraduate", "postgraduate", "research"}

STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "of", "in", "on", "at", "to", "for",
    "with", "from", "by", "my", "our", "your", "is", "are", "was", "were", "am", "be",
    "been", "being", "have", "has", "had", "do", "does", "did", "will", "would", "can",
    "could", "shall", "should", "may", "might", "must", "i", "we", "you", "they", "he",
    "she", "it", "this", "that", "these", "those", "as", "about", "into", "over", "under",
    "again", "then", "once", "here", "there", "all", "any", "each", "some", "no", "not",
    "very", "own", "so", "than", "too", "also", "just", "very", "more", "most", "other",
    "such", "only", "which", "what", "when", "where", "how", "because", "until", "while",
    "business", "businesses", "company", "companies", "shop", "start", "startup", "run",
    "running", "make", "making", "sell", "selling", "small", "day", "days",
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


def _keywords(text: str) -> set:
    if not text:
        return set()
    words = text.lower().replace("\n", " ").replace(",", " ").replace("&", " ").split()
    result = set()
    for w in words:
        token = w.strip(".,;:!?'\"()[]-")
        if len(token) <= 2 or token in STOPWORDS:
            continue
        result.add(token)
        result.add(_singular(token))
    return result


class AdvancedMatchingService:
    WEIGHTS = MATCH_WEIGHTS

    def _sectors(self, scheme: Scheme) -> list[str]:
        return [s.lower() for s in normalize_list(scheme.sectors)]

    def _states(self, scheme: Scheme) -> list[str]:
        return [s.lower() for s in normalize_list(scheme.states)]

    def _stages(self, scheme: Scheme) -> list[str]:
        return [s.lower() for s in normalize_list(scheme.business_stages)]

    def _supports(self, scheme: Scheme) -> list[str]:
        return [s.lower() for s in normalize_list(scheme.support_types)]

    def _types(self, scheme: Scheme) -> list[str]:
        return [s.lower() for s in normalize_list(scheme.entrepreneur_types)]

    def match_sector(self, profile: EntrepreneurProfile, scheme: Scheme) -> int:
        if not profile.business_sector:
            return 0
        sectors = self._sectors(scheme)
        if profile.business_sector.lower() in sectors:
            return self.WEIGHTS["sector"]
        if "all" in sectors:
            return int(self.WEIGHTS["sector"] * 0.6)
        return 0

    def match_support(self, profile: EntrepreneurProfile, scheme: Scheme) -> int:
        profile_supports = [r.support_type.lower() for r in profile.requirements]
        scheme_supports = self._supports(scheme)
        if any(s in scheme_supports for s in profile_supports):
            return self.WEIGHTS["support"]
        return 0

    def match_location(self, profile: EntrepreneurProfile, scheme: Scheme) -> int:
        if not profile.state:
            return 0
        states = self._states(scheme)
        if profile.state.lower() in states:
            return self.WEIGHTS["location"]
        if "all" in states:
            return int(self.WEIGHTS["location"] * 0.6)
        return 0

    def match_stage(self, profile: EntrepreneurProfile, scheme: Scheme) -> int:
        stage_map = {
            "idea": "planning",
            "new": "planning",
            "planning": "planning",
            "existing": "existing",
            "expanding": "expanding",
        }
        profile_stage = stage_map.get(profile.business_stage.lower() if profile.business_stage else "", "")
        if profile_stage and profile_stage in self._stages(scheme):
            return self.WEIGHTS["stage"]
        return 0

    def extract_entrepreneur_types(self, profile: EntrepreneurProfile) -> list[str]:
        types = ["general"]
        gender = (profile.gender or "").lower()
        if gender == "female":
            types.append("woman")
        category = (profile.social_category or "").lower()
        if category in ("sc", "st", "obc", "minority", "pwd"):
            types.append(category)
        age = (getattr(profile, "age_group", None) or "").strip().lower()
        if age in ("18-25", "26-35"):
            types.append("youth")
        return types

    def match_entrepreneur_type(self, profile: EntrepreneurProfile, scheme: Scheme) -> int:
        profile_types = self.extract_entrepreneur_types(profile)
        scheme_types = self._types(scheme)
        if any(t in scheme_types for t in profile_types):
            return self.WEIGHTS["entrepreneur_type"]
        return 0

    def _scheme_text(self, scheme: Scheme) -> str:
        parts = [
            scheme.description or "",
            " ".join(str(x) for x in normalize_list(scheme.benefits)),
            " ".join(str(x) for x in normalize_list(scheme.eligibility)),
            scheme.department or "",
        ]
        return " ".join(parts)

    def match_description(self, profile: EntrepreneurProfile, scheme: Scheme) -> int:
        weighted = self.WEIGHTS.get("description", 0)
        if not weighted or not profile.description:
            return 0
        if getattr(profile, "ai_confirmed", False) and getattr(profile, "ai_tags", None):
            profile_source = " ".join(str(t) for t in profile.ai_tags)
        else:
            profile_source = profile.description
        profile_words = _keywords(profile_source)
        scheme_words = _keywords(self._scheme_text(scheme))
        if not profile_words or not scheme_words:
            return 0
        overlap = profile_words & scheme_words
        if len(overlap) >= 2:
            return weighted
        if len(overlap) == 1:
            return weighted // 2
        return 0

    def get_matched_criteria(self, breakdown: dict) -> List[str]:
        labels = {
            "sector_match": "sector",
            "support_match": "support",
            "location_match": "location",
            "stage_match": "business stage",
            "entrepreneur_type_match": "entrepreneur category",
            "description_match": "business description",
            "targeted_match": "targeted concessional scheme",
        }
        return [labels[k] for k, v in breakdown.items() if v and k in labels]

    # ---- Channel-finance hard eligibility rules ----
    def _family_income_value(self, profile: EntrepreneurProfile) -> Optional[int]:
        band = (profile.annual_family_income or "").strip()
        return FAMILY_INCOME_BANDS.get(band)

    def hard_eligibility(self, profile: EntrepreneurProfile, scheme: Scheme) -> tuple[bool, Optional[str]]:
        """Return (eligible, reason). Reason is non-empty only when ineligible."""
        scheme_types = self._types(scheme)
        if scheme_types and "general" not in scheme_types:
            user_types = self.extract_entrepreneur_types(profile)
            if "woman" in scheme_types and (profile.gender or "").lower() != "female":
                return False, "This scheme is reserved for women applicants"
            if not any(t in scheme_types for t in user_types):
                return False, "This scheme is reserved for a specific category, gender or age group that does not match your profile"

        sc_scheme = bool(scheme.loan_category) and "sc" in self._types(scheme)
        if sc_scheme and (profile.social_category or "").lower() != "sc":
            return False, "This concessional scheme is reserved for Scheduled Caste (SC) applicants"

        ceiling = scheme.income_ceiling
        income_value = self._family_income_value(profile)
        if ceiling and income_value is not None and income_value > ceiling:
            return False, f"Annual family income exceeds the ₹{ceiling / 100000:.1f}L ceiling for this scheme"

        cost = profile.estimated_project_cost
        if cost:
            cat_ceiling = LOAN_CATEGORY_COST_CEILING.get(scheme.loan_category) if scheme.loan_category else None
            if cat_ceiling and cost > cat_ceiling:
                return False, "Project cost exceeds this scheme's lending limit"
            if scheme.max_project_cost and cost > scheme.max_project_cost:
                return False, "Project cost exceeds this scheme's funded-project limit"

        if scheme.loan_category == "education":
            edu = (profile.education_status or "").lower()
            sector = (profile.business_sector or "").lower()
            if edu not in EDUCATION_PURSUING and sector != "education":
                return False, "This is an education loan for students pursuing higher education or studies"
        return True, None

    def match_targeted(self, profile: EntrepreneurProfile, scheme: Scheme) -> int:
        if not scheme.loan_category:
            return 0
        if (profile.social_category or "").lower() == "sc":
            return 8
        return 0

    def identify_gap(self, profile: EntrepreneurProfile, scheme: Scheme) -> Optional[str]:
        needs_collateral = any(
            "collateral" in (e or "").lower() for e in normalize_list(scheme.eligibility)
        )
        if scheme.loan_max and profile.annual_revenue:
            try:
                revenue_band_lower = {
                    "none": 0, "under_10l": 0, "10l_50l": 1000000,
                    "50l_1cr": 5000000, "above_1cr": 10000000,
                    "0_1": 0, "1_10": 0, "50l_plus": 5000000,
                }.get(profile.annual_revenue, 0)
                if scheme.loan_max > 5000000 and revenue_band_lower < 1000000:
                    return "Higher loan schemes may require revenue proof above your current band"
            except Exception:
                pass
        if needs_collateral:
            return "A collateral guarantee may be required for this scheme"
        return None

    def calculate_match(self, profile: EntrepreneurProfile, scheme: Scheme) -> dict:
        breakdown = {
            "sector_match": self.match_sector(profile, scheme),
            "support_match": self.match_support(profile, scheme),
            "location_match": self.match_location(profile, scheme),
            "stage_match": self.match_stage(profile, scheme),
            "entrepreneur_type_match": self.match_entrepreneur_type(profile, scheme),
            "description_match": self.match_description(profile, scheme),
            "targeted_match": self.match_targeted(profile, scheme),
        }
        total = sum(breakdown.values())
        if total >= 90:
            level = "Excellent Match"
        elif total >= 75:
            level = "Strong Match"
        elif total >= 60:
            level = "Possible Match"
        else:
            level = "Low Match"
        return {
            "score": total,
            "level": level,
            "breakdown": breakdown,
            "matched_criteria": self.get_matched_criteria(breakdown),
            "gap": self.identify_gap(profile, scheme),
        }

    def rank_recommendations(self, profile: EntrepreneurProfile, schemes: List[Scheme]) -> List[dict]:
        recommendations = []
        for scheme in schemes:
            eligible, block_reason = self.hard_eligibility(profile, scheme)
            if not eligible:
                continue
            match_info = self.calculate_match(profile, scheme)
            if match_info["score"] < 40:
                continue
            recommendations.append({
                "scheme": scheme,
                "match_score": match_info["score"],
                "match_level": match_info["level"],
                "matched_criteria": match_info["matched_criteria"],
                "match_breakdown": match_info["breakdown"],
                "gap": match_info["gap"],
                "funding_range": self._funding_range(scheme),
                "processing_time": f"{scheme.processing_days} days" if scheme.processing_days else "Varies",
            })
        recommendations.sort(key=lambda x: (x["match_score"], self._specificity(x["scheme"])), reverse=True)
        return recommendations

    def _specificity(self, scheme: Scheme) -> int:
        sectors, states = self._sectors(scheme), self._states(scheme)
        return (0 if "all" in sectors else 1) + (0 if "all" in states else 1)

    def _funding_range(self, scheme: Scheme) -> str:
        if scheme.loan_min is None and scheme.loan_max is None:
            return "Varies"
        if scheme.loan_min is None:
            return f"Upto ₹{scheme.loan_max / 100000:.0f}L"
        if scheme.loan_max is None:
            return f"From ₹{scheme.loan_min / 100000:.1f}L"
        return f"₹{scheme.loan_min / 100000:.1f}L - ₹{scheme.loan_max / 100000:.0f}L"


class RecommendationService:
    def __init__(self, db: Session):
        self.db = db

    def get_recommendations(self, profile: EntrepreneurProfile, min_score: int = 40,
                            max_results: int = 15, language: str = "en",
                            override_sector: str | None = None,
                            override_state: str | None = None,
                            override_stage: str | None = None,
                            override_revenue: str | None = None) -> dict:
        if override_sector:
            profile.business_sector = override_sector
        if override_state:
            profile.state = override_state
        if override_stage:
            profile.business_stage = override_stage
        if override_revenue:
            profile.annual_revenue = override_revenue

        if getattr(profile, "ai_confirmed", False) and profile.ai_sector and not override_sector:
            profile.business_sector = profile.ai_sector

        schemes = self.db.query(Scheme).all()
        matcher = AdvancedMatchingService()
        ranked = matcher.rank_recommendations(profile, schemes)

        items = []
        for rec in ranked[:max_results]:
            if rec["match_score"] < min_score:
                continue
            scheme = rec["scheme"]
            items.append({
                "scheme_id": scheme.id,
                "scheme_name": scheme.name,
                "match_score": rec["match_score"],
                "match_level": rec["match_level"],
                "matched_criteria": rec["matched_criteria"],
                "match_breakdown": rec["match_breakdown"],
                "possible_gap": rec["gap"],
                "explanation": "",
                "funding_range": rec["funding_range"],
                "processing_time": rec["processing_time"],
                "scheme": scheme,
            })

        return {
            "recommendations": items,
            "total_schemes": len(items),
            "profile_summary": {
                "sector": profile.business_sector,
                "state": profile.state,
                "business_stage": profile.business_stage,
                "annual_revenue": profile.annual_revenue,
                "support_needs": [r.support_type for r in profile.requirements],
                "language": language,
            },
        }