from typing import Dict, List, Optional

from pydantic import BaseModel

from app.schemas.scheme import SchemeListItem


class MatchBreakdown(BaseModel):
    sector_match: int = 0
    support_match: int = 0
    location_match: int = 0
    stage_match: int = 0
    entrepreneur_type_match: int = 0
    description_match: int = 0
    total_score: int = 0


class RecommendationRequest(BaseModel):
    sector: Optional[str] = None
    state: Optional[str] = None
    business_stage: Optional[str] = None
    annual_revenue: Optional[str] = None
    entrepreneur_type: Optional[str] = None
    support_needs: List[str] = []
    description: Optional[str] = None
    language: Optional[str] = "en"
    min_score: Optional[int] = 40
    max_results: Optional[int] = 15


class RecommendationItem(BaseModel):
    scheme_id: int
    scheme_name: str
    match_score: int
    match_level: str
    matched_criteria: List[str]
    match_breakdown: MatchBreakdown
    possible_gap: Optional[str] = None
    explanation: str = ""
    funding_range: str = ""
    processing_time: str = ""
    scheme: Optional[SchemeListItem] = None


class RecommendationResponse(BaseModel):
    recommendations: List[RecommendationItem]
    total_schemes: int
    profile_summary: Dict


class PreferencesOut(BaseModel):
    language: str
    theme: str


class PreferencesUpdate(BaseModel):
    language: Optional[str] = None
    theme: Optional[str] = None