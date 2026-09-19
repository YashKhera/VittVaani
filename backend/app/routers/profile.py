from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.profile import ProfileCreateRequest, ProfileResponse, ProfileUpdateRequest
from app.services.matching_service import AdvancedMatchingService
from app.services.profile_service import ProfileService

router = APIRouter(prefix="/profile", tags=["profile"])


def _to_response(profile) -> ProfileResponse:
    return ProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        full_name=profile.full_name or "",
        phone_number=profile.phone_number or "",
        state=profile.state or "",
        district=profile.district or "",
        age_group=profile.age_group or "",
        gender=profile.gender or "",
        social_category=profile.social_category or "",
        annual_family_income=profile.annual_family_income or "",
        education_status=profile.education_status or "not_applicable",
        estimated_project_cost=profile.estimated_project_cost,
        project_type=profile.project_type or "business",
        ideal_loan_category=AdvancedMatchingService().ideal_loan_category(profile),
        business_name=profile.business_name or "",
        business_sector=profile.business_sector or "",
        business_stage=profile.business_stage or "",
        annual_revenue=profile.annual_revenue or "",
        employee_count=profile.employee_count or "",
        description=profile.description or None,
        ai_sector=profile.ai_sector or None,
        ai_tags=(profile.ai_tags or []) if profile.ai_tags else [],
        ai_summary_en=profile.ai_summary_en or None,
        ai_summary_hi=profile.ai_summary_hi or None,
        ai_confirmed=bool(profile.ai_confirmed),
        language_preference=profile.language_preference or "en",
        theme_preference=profile.theme_preference or "light",
        support_needs=[r.support_type for r in profile.requirements],
    )


@router.post("", response_model=ProfileResponse)
def create_profile(payload: ProfileCreateRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = ProfileService(db).create(current_user, payload)
    return _to_response(profile)


@router.get("", response_model=ProfileResponse)
def get_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = ProfileService(db).get(current_user)
    return _to_response(profile)


@router.put("", response_model=ProfileResponse)
def update_profile(payload: ProfileUpdateRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = ProfileService(db).update(current_user, payload)
    return _to_response(profile)