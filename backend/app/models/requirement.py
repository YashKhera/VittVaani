from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Requirement(Base):
    __tablename__ = "requirements"

    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("entrepreneur_profiles.id"), index=True)
    support_type = Column(String(50))
    description = Column(String, nullable=True)

    profile = relationship("EntrepreneurProfile", back_populates="requirements")