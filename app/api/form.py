from fastapi import Depends, APIRouter
from fastapi.responses import Response

from app.auth import get_current_user
from app.dto.user import UserDTO
from app.models.form import FormStatus
from app.schemas.form import FormCreate, ModFormStatus
from app.schemas.user import UserOut
from app.service.dependencies import get_form_service
from app.service.form import FormService

form_router = APIRouter(
    prefix="/form",
    tags=["form"]
)

@form_router.post("/{user_id}/registration", status_code=204)
async def create_form(
    payload: FormCreate,
    current_user: UserDTO = Depends(get_current_user),
    form_service: FormService = Depends(get_form_service)
):
    return await form_service.create_form(current_user, payload)

@form_router.post("/{user_id}/login", status_code=200)
async def update_form_status(
    form_id: int,
    new_form_status: ModFormStatus,
    current_user: UserDTO = Depends(get_current_user),
    form_service: FormService = Depends(get_form_service)
):
    updated_form = await form_service.update_form_status(form_id, new_form_status, current_user)
    return updated_form