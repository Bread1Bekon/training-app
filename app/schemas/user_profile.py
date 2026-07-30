from app.dto.form import FormDTO
from app.dto.profile import ProfileDTO
from pydantic import BaseModel, ConfigDict

from app.schemas.user import UserOut


class UserProfileResponse(BaseModel):
    user: UserOut
    profile: ProfileDTO | None = None
    form: FormDTO | None = None

    model_config = ConfigDict(from_attributes=True)
