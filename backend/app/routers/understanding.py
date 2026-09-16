from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.profile import EntrepreneurProfile
from app.models.requirement import Requirement
from app.models.user import User
from app.schemas.understanding import (
    ApplyFromDescriptionRequest,
    ConfirmUnderstandingRequest,
    UnderstandRequest,
    UnderstandResponse,
)
from app.services.understanding_service import understanding_service

router = APIRouter(prefix="/ai", tags=["ai-understanding"])


def _get_profile(db: Session, user: User) -> EntrepreneurProfile:
    profile = db.query(EntrepreneurProfile).filter(EntrepreneurProfile.user_id == user.id).first()
    if profile is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please complete your profile first")
    return profile


def _sync_requirements(db: Session, profile: EntrepreneurProfile, support_needs: list[str]) -> None:
    if not support_needs:
        return
    existing = {r.support_type for r in db.query(Requirement).filter(Requirement.profile_id == profile.id).all()}
    for need in support_needs:
        if need not in existing:
            db.add(Requirement(profile_id=profile.id, support_type=need))


def _requirement_types(db: Session, profile: EntrepreneurProfile) -> list[str]:
    return [r.support_type for r in db.query(Requirement).filter(Requirement.profile_id == profile.id).all()]


@router.post("/understand", response_model=UnderstandResponse)
def understand(payload: UnderstandRequest, current_user: User = Depends(get_current_user)):
    result = understanding_service.understand(payload.description or "", payload.language or "en")
    return UnderstandResponse(
        sector=result.get("sector"),
        tags=result.get("tags") or [],
        stage=result.get("stage"),
        support_needs=result.get("support_needs") or [],
        summary_en=result.get("summary_en") or "",
        summary_hi=result.get("summary_hi") or "",
        summary_loc=result.get("summary_loc") or "",
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
    if payload.stage and not profile.business_stage:
        profile.business_stage = payload.stage
    _sync_requirements(db, profile, payload.support_needs)
    db.commit()
    return UnderstandResponse(
        sector=profile.ai_sector,
        tags=profile.ai_tags or [],
        stage=profile.business_stage,
        support_needs=_requirement_types(db, profile),
        summary_en=profile.ai_summary_en or "",
        summary_hi=profile.ai_summary_hi or "",
        summary_loc="",
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
        stage=profile.business_stage,
        support_needs=_requirement_types(db, profile),
        summary_en=profile.ai_summary_en or "",
        summary_hi=profile.ai_summary_hi or "",
        provider=understanding_service.provider,
    )


@router.post("/apply-from-description", response_model=UnderstandResponse)
def apply_from_description(
    payload: ApplyFromDescriptionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = understanding_service.understand(payload.description or "", payload.language or "en")
    ai_sector = result.get("sector")
    stage = result.get("stage")
    tags = result.get("tags") or []
    needs = result.get("support_needs") or []
    summary_en = result.get("summary_en") or ""
    summary_hi = result.get("summary_hi") or ""

    profile = db.query(EntrepreneurProfile).filter(EntrepreneurProfile.user_id == current_user.id).first()
    if not profile:
        name = (current_user.email or "").split("@")[0].strip().replace("_", " ").replace(".", " ").title()
        profile = EntrepreneurProfile(
            user_id=current_user.id,
            full_name=name or "User",
            phone_number=current_user.phone_number or "",
            state=payload.state or "all",
            social_category=payload.social_category or "general",
            annual_family_income=payload.annual_family_income or "",
            education_status=payload.education_status or "not_applicable",
            estimated_project_cost=payload.estimated_project_cost,
            business_sector=ai_sector or "all",
            business_stage=stage or "new",
            description=payload.description,
        )
        db.add(profile)
    else:
        if payload.description:
            profile.description = payload.description
        if payload.social_category:
            profile.social_category = payload.social_category
        if payload.state:
            profile.state = payload.state
        if payload.annual_family_income is not None:
            profile.annual_family_income = payload.annual_family_income
        if payload.education_status is not None:
            profile.education_status = payload.education_status
        if payload.estimated_project_cost is not None:
            profile.estimated_project_cost = payload.estimated_project_cost
        if ai_sector and not profile.business_sector:
            profile.business_sector = ai_sector
        if stage and not profile.business_stage:
            profile.business_stage = stage

    db.flush()
    profile.ai_sector = ai_sector
    profile.ai_tags = tags
    profile.ai_summary_en = summary_en
    profile.ai_summary_hi = summary_hi
    profile.ai_confirmed = True
    _sync_requirements(db, profile, needs)
    db.commit()
    profile = db.query(EntrepreneurProfile).filter(EntrepreneurProfile.user_id == current_user.id).first()
    return UnderstandResponse(
        sector=profile.ai_sector,
        tags=profile.ai_tags or [],
        stage=profile.business_stage,
        support_needs=_requirement_types(db, profile),
        summary_en=profile.ai_summary_en or "",
        summary_hi=profile.ai_summary_hi or "",
        summary_loc=result.get("summary_loc") or "",
        provider=understanding_service.provider,
    )
