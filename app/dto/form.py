from pydantic import BaseModel, ConfigDict

from app.schemas.form import FormStatusEnum
from app.schemas.skill import SkillOut


class FormDTO(BaseModel):
    id: int
    description: str
    user_id: int
    status: FormStatusEnum
    skills: list[SkillOut] = []

    model_config = ConfigDict(from_attributes=True)