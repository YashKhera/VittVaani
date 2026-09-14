from datetime import datetime

from sqlalchemy import JSON, Boolean, Column, DateTime, Float, Integer, String
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

    # ---- Channel Finance / concessional lending parameters ----
    loan_category = Column(String(30), nullable=True)          # micro_finance | term_loan | education
    channel_financed = Column(Boolean, default=False)          # routed via Channel Finance System
    interest_rate_min = Column(Float, nullable=True)           # % p.a. (concessional floor)
    interest_rate_max = Column(Float, nullable=True)           # % p.a. ceiling
    moratorium_min_months = Column(Integer, nullable=True)
    moratorium_max_months = Column(Integer, nullable=True)
    max_coverage_pct = Column(Integer, nullable=True)          # % of project cost fundable (<= 90)
    max_project_cost = Column(Integer, nullable=True)          # max project cost this scheme covers (INR)
    tenure_min_months = Column(Integer, nullable=True)
    tenure_max_months = Column(Integer, nullable=True)
    income_ceiling = Column(Integer, nullable=True)            # max annual family income (INR)

    official_url = Column(String(500))
    application_url = Column(String(500))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    saved_by = relationship("SavedScheme", back_populates="scheme", cascade="all, delete-orphan")