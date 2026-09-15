import concurrent.futures
import json
import re

from app.config import settings
from app.services.gemini_client import call_gemini_text
from data.dynamic_questions import (
    COMMON_QUESTIONS,
    EDUCATION_QUESTIONS,
    SECTOR_QUESTIONS,
)

STAGE_NEW = {"new", "idea", "planning"}
STAGE_EXISTING = {"existing", "expanding"}

STUDENT_STATUSES = {"diploma", "undergraduate", "postgraduate", "research"}

MAX_SECTOR_QUESTIONS = 4
MAX_EDUCATION_QUESTIONS = 3
MAX_COMMON_QUESTIONS = 3
MAX_TOTAL_QUESTIONS = 8

# The AI generator is a nice-to-have; the page must never hang on it. Bound it
# so the questionnaire always loads fast and gracefully falls back to the bank.
_AI_TIMEOUT_SECONDS = 6

_MAX_ID = 40
_MAX_TEXT = 160
_AI_TYPES = {"single", "multi", "text"}


def _stage_set(value: str) -> set:
    if value in STAGE_NEW:
        return STAGE_NEW
    if value in STAGE_EXISTING:
        return STAGE_EXISTING
    return {value}


def _matches(q: dict, profile) -> bool:
    sectors = q.get("sectors")
    if sectors and profile.business_sector not in sectors:
        return False
    stages = q.get("stages")
    if stages:
        if not profile.business_stage or _stage_set(profile.business_stage).isdisjoint(stages):
            return False
    if q.get("education_required") and profile.education_status not in STUDENT_STATUSES:
        return False
    return True


def _bank_questions(profile, answered_ids: set) -> list[dict]:
    """Select the curated bank questions that fit this applicant."""

    def take(source, limit, out):
        added = 0
        for q in source:
            if added >= limit:
                break
            if q["id"] in answered_ids:
                continue
            if _matches(q, profile):
                out.append(q)
                added += 1

    selected: list[dict] = []

    sector_list = SECTOR_QUESTIONS.get(profile.business_sector or "", [])
    take(sector_list, MAX_SECTOR_QUESTIONS, selected)
    edu_added = 0
    for q in EDUCATION_QUESTIONS:
        if edu_added >= MAX_EDUCATION_QUESTIONS or len(selected) >= MAX_TOTAL_QUESTIONS:
            break
        # The education sector already asks a "which course" question; don't
        # repeat the same concept from the education-loan gating group.
        if profile.business_sector == "education" and q["id"] == "ed_course_goal":
            continue
        if q["id"] in answered_ids:
            continue
        if _matches(q, profile):
            selected.append(q)
            edu_added += 1
    take(COMMON_QUESTIONS, MAX_COMMON_QUESTIONS, selected)
    return selected[:MAX_TOTAL_QUESTIONS]


def _llm_prompt(profile, answered_ids: set) -> str:
    sector = profile.business_sector or "general small business"
    stage = profile.business_stage or "starting"
    income = profile.annual_family_income or "unknown"
    cat = profile.social_category or "general"
    return (
        "You design a warm, quick questionnaire for an Indian entrepreneur using a loan-scheme "
        "assistant. Ask ONLY genuinely useful follow-up questions that are NOT already known. "
        "Never re-ask: name, phone, age, gender, state, sector, business stage, annual revenue, "
        "social category, family income, education status, project cost.\n"
        f"Their business sector: {sector}. Business stage: {stage} (meaning: new = just starting, "
        "existing = already running). Family income band: {income}. Category: {cat}. "
        f"Already answered ids to skip: {sorted(answered_ids) or 'none'}.\n\n"
        "Return ONLY a valid JSON array of up to 6 questions. Each question object: "
        '{"id": "snake_case_unique", "type": "single"|"multi"|"text", '
        '"title": {"en": "...", "hi": "लघु हिंदी"}, '
        '"help": {"en": "optional hint", "hi": "optional hint"}, '
        '"options": [{"value": "snake_case", "en": "...", "hi": "..."}]}. '
        "For type text, options may be omitted. Questions must be relevant to their sector and "
        "stage (e.g. for food processing ask about raw material, batches, certification, capacity; "
        "for a new business ask about start-up capital, premises, licenses). Keep options short."
    )


def _parse_llm(raw: str) -> list[dict]:
    if not raw:
        return []
    text = raw.strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.IGNORECASE)
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\[[\s\S]*\]", text)
        if not match:
            return []
        try:
            data = json.loads(match.group(0))
        except json.JSONDecodeError:
            return []
    if not isinstance(data, list):
        return []

    cleaned: list[dict] = []
    seen: set = {}
    for item in data:
        if not isinstance(item, dict):
            continue
        qid = str(item.get("id") or "")[: _MAX_ID]
        qtype = item.get("type")
        title = item.get("title") or {}
        if not qid or qtype not in _AI_TYPES or qid in seen:
            continue
        if not isinstance(title, dict) or not title.get("en"):
            continue
        seen[qid] = True
        q = {
            "id": qid,
            "type": qtype,
            "title": {
                "en": str(title.get("en"))[:_MAX_TEXT],
                "hi": str((title.get("hi") or title.get("en")))[:_MAX_TEXT],
            },
        }
        help_text = item.get("help")
        if help_text:
            help_text = help_text if isinstance(help_text, dict) else {"en": help_text, "hi": help_text}
            q["help"] = {
                "en": str(help_text.get("en") or "")[:_MAX_TEXT],
                "hi": str((help_text.get("hi") or help_text.get("en") or ""))[:_MAX_TEXT],
            }
        options = []
        for opt in (item.get("options") or [])[:6]:
            if not isinstance(opt, dict) or not opt.get("value"):
                continue
            options.append({
                "value": str(opt["value"])[:40],
                "en": str(opt.get("en") or opt["value"])[:_MAX_TEXT],
                "hi": str((opt.get("hi") or opt.get("en") or opt["value"]))[:_MAX_TEXT],
            })
        if qtype in {"single", "multi"} and not options:
            continue
        if options:
            q["options"] = options
        cleaned.append(q)
        if len(cleaned) >= MAX_TOTAL_QUESTIONS:
            break
    return cleaned


class DynamicQuestionService:
    """Decides the next, genuinely relevant questions to ask.

    Tries AI generation first (personalised, immersive), and falls back to a
    curated bank when the model is unavailable or the quota is exhausted.
    """

    def get_dynamic_questions(self, profile, answers: dict) -> tuple[list[dict], str]:
        answered_ids = {str(k) for k in (answers or {}).keys()}
        questions, source = self._ai_questions(profile, answered_ids)
        if questions:
            return questions, source
        return _bank_questions(profile, answered_ids), "bank"

    def _ai_questions(self, profile, answered_ids: set) -> tuple[list[dict], str]:
        if not settings.GEMINI_API_KEY:
            return [], "bank"
        pool = None
        try:
            pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)
            future = pool.submit(call_gemini_text, _llm_prompt(profile, answered_ids), 1600)
            raw = future.result(timeout=_AI_TIMEOUT_SECONDS)
        except Exception:
            return [], "bank"
        finally:
            if pool is not None:
                pool.shutdown(wait=False)
        questions = [q for q in _parse_llm(raw) if q["id"] not in answered_ids][:MAX_TOTAL_QUESTIONS]
        return questions, "ai" if questions else "bank"