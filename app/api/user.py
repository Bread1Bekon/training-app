from fastapi import Depends, APIRouter
from fastapi.responses import Response

from app.api.form import form_router
from app.schemas.user import UserCreate, UserOut, LoginRequest, LoginResponse
from app.service.dependencies import get_user_service
from app.service.user import UserService

user_router = APIRouter(
    prefix="/user",
    tags=["user"]
)
user_router.include_router(form_router)

@user_router.post("/", response_model=UserOut, status_code=201)
async def create_user(
    payload: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.create_user(payload)

@user_router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    await user_service.delete_user(user_id)
    return Response(status_code=204)

@user_router.post("/{user_id}", response_model=LoginResponse, status_code=200)
async def log_in(
    data: LoginRequest,
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.log_in(str(data.email), data.password)


@user_router.post("/{user_id}/stats", status_code=200)
async def user_validation_check():
    pass

