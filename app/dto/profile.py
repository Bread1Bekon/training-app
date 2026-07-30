from datetime import date
from pydantic import BaseModel, ConfigDict


class ProfileDTO(BaseModel):
    id: int
    user_id: int
    bio: str | None = None
    avatar: str | None = None
    city: str | None = None
    account_age: date | None = None

    model_config = ConfigDict(from_attributes=True)
