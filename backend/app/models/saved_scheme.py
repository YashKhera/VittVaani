from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class SavedScheme(Base):
    __tablename__ = "saved_schemes"
    __table_args__ = (UniqueConstraint("user_id", "scheme_id", name="uq_user_scheme"),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    scheme_id = Column(Integer, ForeignKey("schemes.id"), index=True)
    saved_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="saved_schemes")
    scheme = relationship("Scheme", back_populates="saved_by")