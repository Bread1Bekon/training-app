from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from .base import Base
from ..enums.user import UserType


class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)  # unique=True
    email = Column(String, unique=True)
    password = Column(String)
    access_level = Column(Enum(UserType))

    profile = relationship("ProfileDB", back_populates="user", cascade="all, delete-orphan")
    forms = relationship("Form", back_populates="owner", cascade="all, delete-orphan")
