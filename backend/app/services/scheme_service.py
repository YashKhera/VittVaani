from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.scheme import Scheme
from app.utils.helpers import normalize_list


class SchemeService:
    def __init__(self, db: Session):
        self.db = db

    def list(self, search: str | None = None, sector: str | None = None,
             state: str | None = None, support: str | None = None,
             government_level: str | None = None, skip: int = 0, limit: int = 50) -> tuple[list[Scheme], int]:
        query = self.db.query(Scheme)
        if search:
            query = query.filter(Scheme.name.ilike(f"%{search}%"))
        if sector:
            query = query.filter(or_(Scheme.sectors.contains(sector), Scheme.sectors.contains(["all"])))
        if support:
            query = query.filter(Scheme.support_types.contains(support))
        if government_level:
            query = query.filter(Scheme.government_level == government_level)

        total = query.count()
        schemes = query.offset(skip).limit(limit).all()

        if state:
            schemes = [
                s for s in schemes
                if state in normalize_list(s.states) or "all" in normalize_list(s.states)
            ]

        return schemes, total

    def get(self, scheme_id: int) -> Scheme:
        scheme = self.db.query(Scheme).filter(Scheme.id == scheme_id).first()
        if not scheme:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scheme not found")
        return scheme