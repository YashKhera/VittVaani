from typing import List

from pydantic import BaseModel


class UnderstandRequest(BaseModel):
    description: str = ""
    language: str = "en"


class UnderstandResponse(BaseModel):
    sector: str | None = None
    tags: List[str] = []
    stage: str | None = None
    support_needs: List[str] = []
    summary_en: str = ""
    summary_hi: str = ""
    summary_loc: str = ""
    provider: str = "builtin"


class ConfirmUnderstandingRequest(BaseModel):
    description: str | None = None
    sector: str | None = None
    tags: List[str] = []
    stage: str | None = None
    support_needs: List[str] = []
    summary_en: str = ""
    summary_hi: str = ""
    language: str = "en"


class ApplyFromDescriptionRequest(BaseModel):
    description: str = ""
    social_category: str | None = None
    state: str | None = None
    annual_family_income: str | None = None
    education_status: str | None = None
    estimated_project_cost: int | None = None
    language: str = "en"