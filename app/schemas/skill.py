from enum import Enum

from pydantic import BaseModel, ConfigDict


class SkillTypeEnum(str, Enum):
    learn = "learn"
    teach = "teach"

class SkillCreate(BaseModel):
    name: str
    description: str
    type: SkillTypeEnum

class SkillOut(BaseModel):
    id: int
    name: str
    description: str
    type: SkillTypeEnum

    model_config = ConfigDict(from_attributes=True)