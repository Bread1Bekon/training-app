from pydantic import BaseModel, ConfigDict

from app.enums.form import FormStatus
from app.schemas.skill import SkillOut


class FormDTO(BaseModel):
    id: int
    description: str
    user_id: int
    status: FormStatus
    skills: list[SkillOut] = []

    model_config = ConfigDict(from_attributes=True)