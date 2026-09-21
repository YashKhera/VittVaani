from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.channel_partner import (
    ChannelPartnerOut,
    PartnerEligibilityResponse,
    PartnerListResponse,
    PartnerNearestResponse,
)
from app.services.partner_service import PartnerService

router = APIRouter(prefix="/partners", tags=["partners"])


def _to_out(p) -> ChannelPartnerOut:
    return ChannelPartnerOut.model_validate(p)


@router.get("", response_model=PartnerListResponse)
def list_partners(
    search: str | None = None,
    state: str | None = None,
    city: str | None = None,
    pincode: str | None = None,
    partner_type: str | None = None,
    loan_category: str | None = None,
    min_health: float | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    partners, total = PartnerService(db).search(
        search=search,
        state=state,
        city=city,
        pincode=pincode,
        partner_type=partner_type,
        loan_category=loan_category,
        min_health=min_health,
        skip=skip,
        limit=limit,
    )
    return PartnerListResponse(partners=[_to_out(p) for p in partners], total=total)


@router.get("/nearest", response_model=PartnerNearestResponse)
def nearest_partners(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    max_distance_km: float = Query(50.0, ge=1, le=1000),
    loan_category: str | None = None,
    partner_type: str | None = None,
    limit: int = Query(20, ge=1, le=100),
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    partners = PartnerService(db).nearest(
        lat=lat,
        lon=lon,
        max_distance_km=max_distance_km,
        loan_category=loan_category,
        partner_type=partner_type,
        limit=limit,
    )
    return PartnerNearestResponse(lat=lat, lon=lon, partners=partners, total=len(partners))


@router.get("/eligible", response_model=PartnerEligibilityResponse)
def eligible_partners(
    loan_category: str | None = None,
    state: str | None = None,
    city: str | None = None,
    min_utilization: float = Query(0.0, ge=0, le=100),
    max_npa: float = Query(8.0, ge=0, le=100),
    max_overdue: float = Query(10.0, ge=0, le=100),
    partner_type: str | None = None,
    limit: int = Query(50, ge=1, le=200),
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    partners = PartnerService(db).eligible(
        loan_category=loan_category,
        state=state,
        city=city,
        min_utilization=min_utilization,
        max_npa=max_npa,
        max_overdue=max_overdue,
        partner_type=partner_type,
        limit=limit,
    )
    return PartnerEligibilityResponse(
        partners=[_to_out(p) for p in partners],
        total=len(partners),
        filters={
            "loan_category": loan_category,
            "state": state,
            "city": city,
            "min_utilization": min_utilization,
            "max_npa": max_npa,
            "max_overdue": max_overdue,
            "partner_type": partner_type,
        },
    )


@router.get("/{partner_id}", response_model=ChannelPartnerOut)
def get_partner(partner_id: int, _: User = Depends(get_current_user), db: Session = Depends(get_db)):
    partner = PartnerService(db).get(partner_id)
    return _to_out(partner)