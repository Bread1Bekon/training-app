from fastapi import Depends, APIRouter

from app.auth import get_current_user
from app.dto.user import UserDTO
from app.enums.form import ModFormStatus
from app.schemas.form import FormCreate, FormOut
from app.service.dependencies import get_form_service
from app.service.form import FormService

form_router = APIRouter(
    prefix="/forms",
    tags=["form"]
)

@form_router.post("/", status_code=204)
async def create_form(
    payload: FormCreate,
    current_user: UserDTO = Depends(get_current_user),
    form_service: FormService = Depends(get_form_service)
):
    return await form_service.create_form(current_user, payload)

@form_router.patch("/{form_id}/", status_code=200)
async def update_form_status(
    form_id: int,
    new_form_status: ModFormStatus,
    current_user: UserDTO = Depends(get_current_user),
    form_service: FormService = Depends(get_form_service)
):
    updated_form = await form_service.update_form_status(form_id, new_form_status, current_user)
    return updated_form

@form_router.get("/{form_id}/", status_code=200)
async def get_form_for_moderation(
    form_id: int,
    current_user: UserDTO = Depends(get_current_user),
    form_service: FormService = Depends(get_form_service),
):
    return await form_service.get_form_for_moderation(form_id, current_user)

@form_router.get("/")
async def find_relevant_forms(
    form_service: FormService = Depends(get_form_service),
    current_user: UserDTO = Depends(get_current_user)
):
    return await form_service.find_suitable_forms(current_user.id)
