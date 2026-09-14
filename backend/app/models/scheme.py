from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Scheme(Base):
    __tablename__ = "schemes"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), index=True)
    short_name = Column(String(100), nullable=True)
    government_level = Column(String(20))
    department = Column(String(255))
    description = Column(String)

    sectors = Column(JSON)
    states = Column(JSON)
    business_stages = Column(JSON)
    support_types = Column(JSON)
    entrepreneur_types = Column(JSON)

    benefits = Column(JSON)
    eligibility = Column(JSON)
    documents = Column(JSON)

    loan_min = Column(Integer)
    loan_max = Column(Integer)
    processing_days = Column(Integer)

    official_url = Column(String(500))
    application_url = Column(String(500))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    saved_by = relationship("SavedScheme", back_populates="scheme", cascade="all, delete-orphan")