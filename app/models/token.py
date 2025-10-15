from sqlalchemy import Column, String, Boolean, DateTime
from .base import Base

class TokenDB(Base):
    __tablename__ = 'tokens'
    refresh_token = Column(String, primary_key=True)
    is_valid = Column(Boolean)
    refresh_expires = Column(DateTime)