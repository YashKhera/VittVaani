from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON
from sqlalchemy.orm import relationship

from app.database import Base


class QuestionnaireProgress(Base):
    __tablename__ = "questionnaire_progress"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, index=True, nullable=False)
    answers = Column(JSON, default=dict)
    step = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="questionnaire_progress")
