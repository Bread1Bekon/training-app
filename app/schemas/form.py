from pydantic import BaseModel, ConfigDict
from enum import Enum

from app.enums.form import FormStatus
from app.schemas.skill import SkillCreate, SkillOut

class FormCreate(BaseModel):
    description: str
    skills: list[SkillCreate]

class FormOut(BaseModel):
    id: int
    description: str
    user_id: int
    status: FormStatus
    skills: list[SkillOut] = []

    model_config = ConfigDict(from_attributes=True)
