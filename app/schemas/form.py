from pydantic import BaseModel, ConfigDict
from enum import Enum

from app.schemas.skill import SkillCreate, SkillOut


class FormStatusEnum(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class FormCreate(BaseModel):
    description: str
    skills: list[SkillCreate]

class FormOut(BaseModel):
    id: int
    description: str
    user_id: int
    status: FormStatusEnum
    skills: list[SkillOut] = []

    model_config = ConfigDict(from_attributes=True)
