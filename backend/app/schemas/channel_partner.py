from typing import List, Optional

from pydantic import BaseModel


class ChannelPartnerOut(BaseModel):
    id: int
    name: str
    partner_type: str
    state: str
    city: str
    district: str | None = None
    pincode: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    address: str | None = None
    phone: str | None = None
    email: str | None = None
    website: str | None = None
    loan_categories: List[str] = []
    fund_utilization_pct: float = 0.0
    npa_pct: float = 0.0
    overdue_pct: float = 0.0
    official_url: str | None = None

    class Config:
        from_attributes = True


class PartnerNearestItem(ChannelPartnerOut):
    distance_km: Optional[float] = None


class PartnerListResponse(BaseModel):
    partners: List[ChannelPartnerOut]
    total: int


class PartnerNearestResponse(BaseModel):
    lat: float
    lon: float
    partners: List[PartnerNearestItem]
    total: int


class PartnerEligibilityResponse(BaseModel):
    partners: List[ChannelPartnerOut]
    total: int
    filters: dict = {}