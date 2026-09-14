from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import relationship

from app.database import Base


class EntrepreneurProfile(Base):
    __tablename__ = "entrepreneur_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, index=True)

    full_name = Column(String(255))
    phone_number = Column(String(20))
    state = Column(String(50))
    district = Column(String(50))
    age_group = Column(String(20))
    gender = Column(String(20))
    social_category = Column(String(20))

    # ---- Concessional lending / SC scheme inputs ----
    annual_family_income = Column(String(30), nullable=True)   # band: under_2.5l | 2.5l_5l | above_5l
    education_status = Column(String(30), nullable=True)       # for educational loans
    estimated_project_cost = Column(Integer, nullable=True)    # planned project cost (INR)

    business_name = Column(String(255))
    business_sector = Column(String(50))
    business_stage = Column(String(50))
    annual_revenue = Column(String(50))
    employee_count = Column(String(50))
    description = Column(String, nullable=True)

    ai_sector = Column(String(50), nullable=True)
    ai_tags = Column(JSON, nullable=True)
    ai_summary_en = Column(String, nullable=True)
    ai_summary_hi = Column(String, nullable=True)
    ai_confirmed = Column(Boolean, default=False)

    language_preference = Column(String(10), default="en")
    theme_preference = Column(String(10), default="light")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="profile")
    requirements = relationship("Requirement", back_populates="profile", cascade="all, delete-orphan")