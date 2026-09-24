from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class SchemeExplanation(Base):
    __tablename__ = "scheme_explanations"
    __table_args__ = (
        UniqueConstraint(
            "scheme_id", "language", "criteria_key", name="uq_scheme_explanation_key"
        ),
    )

    id = Column(Integer, primary_key=True)
    scheme_id = Column(Integer, ForeignKey("schemes.id"), index=True)
    language = Column(String(8), nullable=False, default="en")
    criteria_key = Column(String(64), nullable=False)
    explanation = Column(Text, nullable=False, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    scheme = relationship("Scheme", backref="explanations")
