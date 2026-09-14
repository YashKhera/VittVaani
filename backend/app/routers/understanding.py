from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.profile import EntrepreneurProfile
from app.models.user import User
from app.schemas.understanding import ConfirmUnderstandingRequest, UnderstandRequest, UnderstandResponse
from app.services.understanding_service import understanding_service

router = APIRouter(prefix="/ai", tags=["ai-understanding"])


def _get_profile(db: Session, user: User) -> EntrepreneurProfile:
    profile = db.query(EntrepreneurProfile).filter(EntrepreneurProfile.user_id == user.id).first()
    if profile is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please complete your profile first")
    return profile


@router.post("/understand", response_model=UnderstandResponse)
def understand(payload: UnderstandRequest, current_user: User = Depends(get_current_user)):
    result = understanding_service.understand(payload.description or "")
    return UnderstandResponse(
        sector=result.get("sector"),
        tags=result.get("tags") or [],
        summary_en=result.get("summary_en") or "",
        summary_hi=result.get("summary_hi") or "",
        provider=result.get("provider") or "builtin",
    )


@router.post("/confirm", response_model=UnderstandResponse)
def confirm_understanding(
    payload: ConfirmUnderstandingRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = _get_profile(db, current_user)
    profile.description = payload.description if payload.description is not None else profile.description
    profile.ai_sector = payload.sector
    profile.ai_tags = payload.tags or []
    profile.ai_summary_en = payload.summary_en
    profile.ai_summary_hi = payload.summary_hi
    profile.ai_confirmed = True
    db.commit()
    db.refresh(profile)
    return UnderstandResponse(
        sector=profile.ai_sector,
        tags=profile.ai_tags or [],
        summary_en=profile.ai_summary_en or "",
        summary_hi=profile.ai_summary_hi or "",
        provider=understanding_service.provider,
    )


@router.get("/understanding", response_model=UnderstandResponse)
def get_understanding(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = _get_profile(db, current_user)
    return UnderstandResponse(
        sector=profile.ai_sector,
        tags=profile.ai_tags or [],
        summary_en=profile.ai_summary_en or "",
        summary_hi=profile.ai_summary_hi or "",
        provider=understanding_service.provider,
    )