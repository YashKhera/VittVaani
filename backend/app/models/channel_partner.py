from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Float, Integer, String

from app.database import Base


class ChannelPartner(Base):
    __tablename__ = "channel_partners"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), index=True)
    partner_type = Column(String(30), index=True)        # sca | psb | rrb | nbfc_mfi
    level = Column(String(20), default="state")          # state channelizing agency reach
    state = Column(String(50), index=True)               # STATE_KEYS key e.g. "maharashtra"
    city = Column(String(100), index=True)
    district = Column(String(100), nullable=True)
    pincode = Column(String(10), index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    address = Column(String(500), nullable=True)
    phone = Column(String(30), nullable=True)
    email = Column(String(120), nullable=True)
    website = Column(String(500), nullable=True)

    # Which loan categories the partner can originate: micro_finance | term_loan | education
    loan_categories = Column(JSON, default=list)

    # ---- Channel health metrics (0-100) ----
    fund_utilization_pct = Column(Float, default=0.0)    # % of allocated channel funds utilized
    npa_pct = Column(Float, default=0.0)                 # gross NPA % on channel portfolio
    overdue_pct = Column(Float, default=0.0)             # % accounts overdue (>90 days)

    official_url = Column(String(500), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)