from pydantic import BaseModel, ConfigDict

from app.enums.form import FormStatus
from app.dto.skill import SkillDTO

class FormDTO(BaseModel):
    id: int
    description: str
    user_id: int
    status: FormStatus
    skills: list[SkillDTO] = []

    model_config = ConfigDict(from_attributes=True)