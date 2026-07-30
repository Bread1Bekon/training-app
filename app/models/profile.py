from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class ProfileDB(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    bio = Column(String, nullable=True)
    avatar = Column(String, nullable=True)
    city = Column(String, nullable=True)
    account_age = Column(Date, nullable=True)

    user = relationship("UserDB", back_populates="profile")
