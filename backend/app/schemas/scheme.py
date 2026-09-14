from typing import List

from pydantic import BaseModel


class SchemeListItem(BaseModel):
    id: int
    name: str
    short_name: str | None = None
    government_level: str
    department: str
    description: str
    sectors: List[str]
    states: List[str]
    business_stages: List[str]
    support_types: List[str]
    entrepreneur_types: List[str]
    loan_min: int | None = None
    loan_max: int | None = None
    processing_days: int | None = None
    loan_category: str | None = None
    channel_financed: bool = False
    interest_rate_min: float | None = None
    interest_rate_max: float | None = None
    moratorium_min_months: int | None = None
    moratorium_max_months: int | None = None
    max_coverage_pct: int | None = None
    max_project_cost: int | None = None
    tenure_min_months: int | None = None
    tenure_max_months: int | None = None
    income_ceiling: int | None = None
    official_url: str | None = None
    application_url: str | None = None

    class Config:
        from_attributes = True


class SchemeDetail(SchemeListItem):
    benefits: List[str] = []
    eligibility: List[str] = []
    documents: List[str] = []


class SchemeListResponse(BaseModel):
    schemes: List[SchemeListItem]
    total: int


class SavedSchemeOut(BaseModel):
    id: int
    scheme: SchemeListItem
    saved_at: str | None = None


class SavedSchemesResponse(BaseModel):
    saved_schemes: List[SavedSchemeOut]
    total: int