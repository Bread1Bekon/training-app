import enum

from sqlalchemy import Column, Integer, String, Enum
from .base import Base

class UserType(str, enum.Enum):
     ORDINARY = "ordinary"
     MODERATOR = "moderator"

class UserDB(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String) #unique=True
    email = Column(String) #unique=True
    password = Column(String)
    access_level = Column(Enum(UserType))

