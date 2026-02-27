from fastapi import Depends, APIRouter
from fastapi.responses import Response

from app.auth import get_current_user
from app.schemas.form import FormCreate
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
    current_user: UserOut = Depends(get_current_user),
    form_service: FormService = Depends(get_form_service)
):
    await form_service.create_form(current_user, payload)
    return Response(status_code=204)