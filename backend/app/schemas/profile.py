from typing import List

from pydantic import BaseModel, Field


class ProfileCreateRequest(BaseModel):
    full_name: str
    phone_number: str = ""
    state: str
    district: str = ""
    age_group: str = ""
    gender: str = "other"
    social_category: str = "general"
    annual_family_income: str = ""
    education_status: str = "not_applicable"
    estimated_project_cost: int | None = None
    business_name: str = ""
    business_sector: str
    business_stage: str = "existing"
    annual_revenue: str = "none"
    employee_count: str = ""
    description: str | None = None
    support_needs: List[str] = Field(default_factory=list)


class ProfileUpdateRequest(BaseModel):
    full_name: str | None = None
    phone_number: str | None = None
    state: str | None = None
    district: str | None = None
    age_group: str | None = None
    gender: str | None = None
    social_category: str | None = None
    annual_family_income: str | None = None
    education_status: str | None = None
    estimated_project_cost: int | None = None
    business_name: str | None = None
    business_sector: str | None = None
    business_stage: str | None = None
    annual_revenue: str | None = None
    employee_count: str | None = None
    description: str | None = None
    support_needs: List[str] | None = None


class RequirementOut(BaseModel):
    support_type: str
    description: str | None = None


class ProfileResponse(BaseModel):
    id: int
    user_id: int
    full_name: str
    phone_number: str
    state: str
    district: str
    age_group: str
    gender: str
    social_category: str
    annual_family_income: str = ""
    education_status: str = "not_applicable"
    estimated_project_cost: int | None = None
    business_name: str
    business_sector: str
    business_stage: str
    annual_revenue: str
    employee_count: str
    description: str | None = None
    ai_sector: str | None = None
    ai_tags: List[str] | None = None
    ai_summary_en: str | None = None
    ai_summary_hi: str | None = None
    ai_confirmed: bool = False
    language_preference: str
    theme_preference: str
    support_needs: List[str] = []

    class Config:
        from_attributes = True