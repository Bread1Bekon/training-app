from app.dto.form import FormDTO
from pydantic import BaseModel, ConfigDict

from app.schemas.user import UserOut


class UserProfileResponse(BaseModel):
    user: UserOut
    form: FormDTO | None = None

    model_config = ConfigDict(from_attributes=True)