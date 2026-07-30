from pydantic import BaseModel, EmailStr, ConfigDict, field_validator

from app.enums.user import UserType


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    access_level: UserType = UserType.ORDINARY

    @field_validator("email")
    def normalize_email(cls, email: EmailStr) -> str:
        return str(email).lower()


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None


class PasswordChange(BaseModel):
    old_password: str
    new_password: str


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
