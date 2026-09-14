from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.profile import EntrepreneurProfile
from app.models.user import User
from app.schemas.recommendation import PreferencesOut, PreferencesUpdate
from app.services.profile_service import ProfileService

router = APIRouter(prefix="/preferences", tags=["preferences"])


@router.get("", response_model=PreferencesOut)
def get_preferences(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(EntrepreneurProfile).filter(EntrepreneurProfile.user_id == current_user.id).first()
    if not profile:
        return PreferencesOut(language="en", theme="light")
    return PreferencesOut(language=profile.language_preference or "en", theme=profile.theme_preference or "light")


@router.put("", response_model=PreferencesOut)
def update_preferences(payload: PreferencesUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(EntrepreneurProfile).filter(EntrepreneurProfile.user_id == current_user.id).first()
    if not profile:
        profile = ProfileService(db).get(current_user)
    if payload.language:
        profile.language_preference = payload.language
    if payload.theme:
        profile.theme_preference = payload.theme
    db.commit()
    return PreferencesOut(language=profile.language_preference or "en", theme=profile.theme_preference or "light")