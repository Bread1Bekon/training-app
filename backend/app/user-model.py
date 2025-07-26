from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class User(BaseModel):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String)
    email: str = Column(String)