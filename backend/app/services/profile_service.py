from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.profile import EntrepreneurProfile
from app.models.requirement import Requirement
from app.models.user import User
from app.schemas.profile import ProfileCreateRequest, ProfileUpdateRequest


def _sync_requirements(db: Session, profile: EntrepreneurProfile, support_needs: list[str]) -> None:
    db.query(Requirement).filter(Requirement.profile_id == profile.id).delete()
    for need in support_needs or []:
        db.add(Requirement(profile_id=profile.id, support_type=need))


class ProfileService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User, payload: ProfileCreateRequest) -> EntrepreneurProfile:
        existing = self.db.query(EntrepreneurProfile).filter(EntrepreneurProfile.user_id == user.id).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Profile already exists")
        profile = EntrepreneurProfile(
            user_id=user.id,
            full_name=payload.full_name,
            phone_number=payload.phone_number,
            state=payload.state,
            district=payload.district,
            age_group=payload.age_group,
            gender=payload.gender,
            social_category=payload.social_category,
            annual_family_income=payload.annual_family_income,
            education_status=payload.education_status,
            estimated_project_cost=payload.estimated_project_cost,
            project_type=payload.project_type,
            business_name=payload.business_name,
            business_sector=payload.business_sector,
            business_stage=payload.business_stage,
            annual_revenue=payload.annual_revenue,
            employee_count=payload.employee_count,
            description=payload.description,
        )
        self.db.add(profile)
        self.db.flush()
        _sync_requirements(self.db, profile, payload.support_needs)
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def get(self, user: User) -> EntrepreneurProfile:
        profile = self.db.query(EntrepreneurProfile).filter(EntrepreneurProfile.user_id == user.id).first()
        if not profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
        return profile

    def update(self, user: User, payload: ProfileUpdateRequest) -> EntrepreneurProfile:
        profile = self.get(user)
        data = payload.model_dump(exclude_unset=True)
        support_needs = data.pop("support_needs", None)
        for field, value in data.items():
            setattr(profile, field, value)
        if support_needs is not None:
            _sync_requirements(self.db, profile, support_needs)
        self.db.commit()
        self.db.refresh(profile)
        return profile