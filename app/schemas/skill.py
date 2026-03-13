from pydantic import BaseModel, ConfigDict

from app.enums.skill import SkillType


class SkillCreate(BaseModel):
    name: str
    description: str
    type: SkillType

class SkillOut(BaseModel):
    id: int
    name: str
    description: str
    type: SkillType

    model_config = ConfigDict(from_attributes=True)