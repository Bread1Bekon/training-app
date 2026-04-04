from pydantic import BaseModel, ConfigDict

from app.enums.skill import SkillType


class SkillDTO(BaseModel):
    id: int
    name: str
    description: str | None
    form_id: int
    type: SkillType

    model_config = ConfigDict(from_attributes=True)