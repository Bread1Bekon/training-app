from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum
from .base import Base
from ..enums.skill import SkillType


class Skill(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True)
    form_id = Column(Integer, ForeignKey('form.id'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    type = Column(Enum(SkillType), nullable=False)