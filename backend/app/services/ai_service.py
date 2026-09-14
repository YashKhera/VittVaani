import json
from typing import Optional

from app.config import settings
from app.models.profile import EntrepreneurProfile
from app.models.scheme import Scheme
from app.services.gemini_client import call_gemini_text


class AIExplanationService:
    def __init__(self):
        self.client = None
        self.enabled = bool(settings.GEMINI_API_KEY or settings.AI_API_KEY)
        if not self.enabled:
            return
        if settings.AI_API_KEY:
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=settings.AI_API_KEY)
            except Exception:
                self.client = None

    @staticmethod
    def _gemini_text(prompt: str) -> str:
        return call_gemini_text(prompt, max_tokens=1024)

    def _fallback(self, profile: EntrepreneurProfile, scheme: Scheme, matched_criteria: list[str], language: str) -> str:
        joined = ", ".join(matched_criteria) if matched_criteria else "no specific matches yet"
        if language == "hi":
            return (
                f"{scheme.name} आपके व्यवसाय के लिए एक अच्छा विकल्प हो सकता है। "
                f"मेल होने के कारण: {joined}। अधिक जानकारी के लिए आधिकारिक लिंक देखें।"
            )
        return (
            f"{scheme.name} looks like a good fit for your business. "
            f"Match factors: {joined}. Check the official link for application details."
        )

    def generate_explanation(self, profile: EntrepreneurProfile, scheme: Scheme,
                             matched_criteria: list[str], language: str = "en") -> str:
        if not self.enabled:
            return self._fallback(profile, scheme, matched_criteria, language)
        prompt = (
            "Generate a brief, helpful explanation (2-3 sentences) of why this government scheme "
            "is a good match for this entrepreneur.\n\n"
            f"Entrepreneur:\n- Sector: {profile.business_sector}\n- Location: {profile.state}\n"
            f"- Business Stage: {profile.business_stage}\n- Gender: {profile.gender}\n"
            f"- Business Description: {profile.description or 'Not provided'}\n"
            f"- AI-understood tags: {', '.join(profile.ai_tags or []) if profile.ai_confirmed else 'none'}\n\n"
            f"Scheme:\n- Name: {scheme.name}\n- Focus: {', '.join(scheme.sectors or [])}\n"
            f"- Support: {', '.join(scheme.support_types or [])}\n\n"
            f"Matched criteria: {', '.join(matched_criteria) if matched_criteria else 'none'}\n\n"
            f"Write in simple, encouraging language. Language: {language}"
        )
        try:
            text = ""
            if settings.GEMINI_API_KEY:
                text = self._gemini_text(prompt)
            if not text and self.client is not None:
                message = self.client.messages.create(
                    model=settings.AI_MODEL,
                    max_tokens=200,
                    messages=[{"role": "user", "content": prompt}],
                )
                text = message.content[0].text
            return text.strip() if text else self._fallback(profile, scheme, matched_criteria, language)
        except Exception:
            return self._fallback(profile, scheme, matched_criteria, language)


ai_service = AIExplanationService()