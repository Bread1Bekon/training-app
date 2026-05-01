from pydantic import BaseModel, ConfigDict

from app.enums.user import UserType


class UserDTO(BaseModel):
    id: int
    name: str
    email: str
    password: str
    access_level: UserType

    model_config = ConfigDict(from_attributes=True)