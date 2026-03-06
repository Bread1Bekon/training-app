import enum

from pydantic import BaseModel, EmailStr, ConfigDict


class UserType(str, enum.Enum):
    ordinary = "ordinary"
    moderator = "moderator"

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    access_level: UserType

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    access_level: UserType

    model_config = ConfigDict(from_attributes=True)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
