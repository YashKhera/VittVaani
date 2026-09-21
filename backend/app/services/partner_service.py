import math

from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.channel_partner import ChannelPartner
from app.schemas.channel_partner import ChannelPartnerOut
from app.utils.helpers import normalize_list


EARTH_RADIUS_KM = 6371.0


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance between two lat/lon points in km."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = (
        math.sin(d_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    )
    return EARTH_RADIUS_KM * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _health_score(partner: ChannelPartner) -> float:
    """Rank partners by channel health: higher utilization-fill, lower NPA/overdue."""
    return (
        float(partner.fund_utilization_pct)
        - 2.0 * float(partner.npa_pct or 0.0)
        - 1.0 * float(partner.overdue_pct or 0.0)
    )


def _to_distance_item(partner: ChannelPartner, dist: float):
    item = ChannelPartnerOut.model_validate(partner).model_dump()
    item["distance_km"] = round(dist, 2)
    return item


class PartnerService:
    def __init__(self, db: Session):
        self.db = db

    def search(
        self,
        search: str | None = None,
        state: str | None = None,
        city: str | None = None,
        pincode: str | None = None,
        partner_type: str | None = None,
        loan_category: str | None = None,
        min_health: float | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> tuple[list[ChannelPartner], int]:
        query = self.db.query(ChannelPartner)
        if search:
            query = query.filter(
                or_(
                    ChannelPartner.name.ilike(f"%{search}%"),
                    ChannelPartner.city.ilike(f"%{search}%"),
                    ChannelPartner.district.ilike(f"%{search}%"),
                )
            )
        if state:
            query = query.filter(ChannelPartner.state == state)
        if city:
            query = query.filter(ChannelPartner.city.ilike(f"%{city}%"))
        if pincode:
            query = query.filter(ChannelPartner.pincode.like(f"%{pincode}%"))
        if partner_type:
            query = query.filter(ChannelPartner.partner_type == partner_type)
        if loan_category:
            query = query.filter(ChannelPartner.loan_categories.contains(loan_category))

        total = query.count()
        partners = query.offset(skip).limit(limit).all()

        if min_health is not None:
            partners = [p for p in partners if _health_score(p) >= min_health]
            total = min(total, len(partners))

        return partners, total

    def get(self, partner_id: int) -> ChannelPartner:
        partner = self.db.query(ChannelPartner).filter(ChannelPartner.id == partner_id).first()
        if not partner:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Channel partner not found"
            )
        return partner

    def nearest(
        self,
        lat: float,
        lon: float,
        max_distance_km: float = 50.0,
        loan_category: str | None = None,
        partner_type: str | None = None,
        limit: int = 20,
    ) -> list[dict]:
        partners = self.db.query(ChannelPartner).all()
        results = []
        for p in partners:
            if p.latitude is None or p.longitude is None:
                continue
            if loan_category and loan_category not in normalize_list(p.loan_categories):
                continue
            if partner_type and p.partner_type != partner_type:
                continue
            dist = haversine_km(lat, lon, float(p.latitude), float(p.longitude))
            if dist <= max_distance_km:
                results.append((dist, p))
        results.sort(key=lambda t: (t[0], -_health_score(t[1])))
        return [_to_distance_item(p, d) for d, p in results[:limit]]

    def eligible(
        self,
        loan_category: str | None = None,
        state: str | None = None,
        city: str | None = None,
        min_utilization: float = 0.0,
        max_npa: float = 8.0,
        max_overdue: float = 10.0,
        partner_type: str | None = None,
        limit: int = 50,
    ) -> list[ChannelPartner]:
        query = self.db.query(ChannelPartner)
        if loan_category:
            query = query.filter(ChannelPartner.loan_categories.contains(loan_category))
        if state:
            query = query.filter(ChannelPartner.state == state)
        if city:
            query = query.filter(ChannelPartner.city.ilike(f"%{city}%"))
        if partner_type:
            query = query.filter(ChannelPartner.partner_type == partner_type)

        partners = query.all()
        filtered = []
        for p in partners:
            util = float(p.fund_utilization_pct or 0.0)
            npa = float(p.npa_pct or 0.0)
            overdue = float(p.overdue_pct or 0.0)
            if util < min_utilization:
                continue
            if npa > max_npa:
                continue
            if overdue > max_overdue:
                continue
            filtered.append(p)
        filtered.sort(key=lambda p: -_health_score(p))
        return filtered[:limit]