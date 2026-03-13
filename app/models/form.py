from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from .base import Base
from ..enums.form import FormStatus


class Form(Base):
    __tablename__ = 'form'
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    status = Column(Enum(FormStatus), default=FormStatus.PENDING, nullable=False)

    skills = relationship("Skill", backref="form", cascade="all, delete-orphan")