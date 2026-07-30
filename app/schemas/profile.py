from datetime import date
from pydantic import BaseModel, ConfigDict

class ProfileUpdate(BaseModel):
    bio: str | None = None
    avatar: str | None = None
    city: str | None = None
    account_age: date | None = None


class ProfileOut(BaseModel):
    id: int
    user_id: int
    bio: str | None = None
    avatar: str | None = None
    city: str | None = None
    account_age: date | None = None

    model_config = ConfigDict(from_attributes=True)
