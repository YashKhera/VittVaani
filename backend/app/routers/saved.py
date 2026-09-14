from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.saved_scheme import SavedScheme
from app.models.scheme import Scheme
from app.models.user import User
from app.schemas.scheme import SavedSchemeOut, SavedSchemesResponse, SchemeListItem
from app.services.scheme_service import SchemeService

router = APIRouter(prefix="/saved-schemes", tags=["saved"])


@router.get("", response_model=SavedSchemesResponse)
def list_saved(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    saved = (
        db.query(SavedScheme)
        .filter(SavedScheme.user_id == current_user.id)
        .order_by(SavedScheme.saved_at.desc())
        .all()
    )
    items = [
        SavedSchemeOut(id=row.id, scheme=SchemeListItem.model_validate(row.scheme), saved_at=str(row.saved_at))
        for row in saved
    ]
    return SavedSchemesResponse(saved_schemes=items, total=len(items))


@router.post("/{scheme_id}", response_model=SavedSchemeOut)
def save_scheme(scheme_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    SchemeService(db).get(scheme_id)
    existing = (
        db.query(SavedScheme)
        .filter(SavedScheme.user_id == current_user.id, SavedScheme.scheme_id == scheme_id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Scheme already saved")
    row = SavedScheme(user_id=current_user.id, scheme_id=scheme_id)
    db.add(row)
    db.commit()
    db.refresh(row)
    scheme: Scheme = db.query(Scheme).filter(Scheme.id == scheme_id).first()
    return SavedSchemeOut(id=row.id, scheme=SchemeListItem.model_validate(scheme), saved_at=str(row.saved_at))


@router.delete("/{scheme_id}")
def remove_saved(scheme_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = (
        db.query(SavedScheme)
        .filter(SavedScheme.user_id == current_user.id, SavedScheme.scheme_id == scheme_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Saved scheme not found")
    db.delete(row)
    db.commit()
    return {"message": "Removed from saved schemes"}