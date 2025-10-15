from sqlalchemy import Column, Integer, String
from .base import Base

class UserDB(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

