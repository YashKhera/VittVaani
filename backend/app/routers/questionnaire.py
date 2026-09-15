from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.profile import EntrepreneurProfile
from app.models.questionnaire_progress import QuestionnaireProgress
from app.models.user import User
from app.schemas.questionnaire import (
    DynamicQuestionRequest,
    DynamicQuestionResponse,
    ProgressPayload,
    ProgressResponse,
)
from app.services.dynamic_question_service import DynamicQuestionService

router = APIRouter(prefix="/questionnaire", tags=["questionnaire"])


def _get_or_none(db: Session, user: User) -> QuestionnaireProgress | None:
    return db.query(QuestionnaireProgress).filter(QuestionnaireProgress.user_id == user.id).first()


@router.get("/progress", response_model=ProgressResponse)
def get_progress(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    record = _get_or_none(db, current_user)
    if not record:
        return ProgressResponse(answers={}, step=0)
    return ProgressResponse(answers=record.answers or {}, step=record.step or 0)


@router.put("/progress", response_model=ProgressResponse)
def save_progress(payload: ProgressPayload, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    record = _get_or_none(db, current_user)
    if not record:
        record = QuestionnaireProgress(user_id=current_user.id, answers=payload.answers, step=payload.step)
        db.add(record)
    else:
        record.answers = payload.answers
        record.step = payload.step
    db.commit()
    db.refresh(record)
    return ProgressResponse(answers=record.answers or {}, step=record.step or 0)


@router.delete("/progress", status_code=status.HTTP_204_NO_CONTENT)
def clear_progress(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.query(QuestionnaireProgress).filter(QuestionnaireProgress.user_id == current_user.id).delete()
    db.commit()
    return None


@router.post("/dynamic", response_model=DynamicQuestionResponse)
def get_dynamic_questions(
    payload: DynamicQuestionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return the next genuinely relevant questions for this applicant.

    Profile basics (name, sector, stage, income, category…) are never re-asked;
    the returned questions are personalised follow-ups derived from the bank,
    or AI-generated when the model is available.
    """
    profile = (
        db.query(EntrepreneurProfile)
        .filter(EntrepreneurProfile.user_id == current_user.id)
        .first()
    )
    if profile is None:
        return DynamicQuestionResponse(questions=[])
    questions, source = DynamicQuestionService().get_dynamic_questions(profile, payload.answers)
    return DynamicQuestionResponse(questions=questions, source=source)
