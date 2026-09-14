from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.database import Base


class OtpCode(Base):
    __tablename__ = "otp_codes"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), index=True, nullable=False)
    code_hash = Column(String(128), nullable=False)
    purpose = Column(String(50), default="password_reset", nullable=False)
    attempts = Column(Integer, default=0, nullable=False)
    used = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)