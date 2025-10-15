from fastapi.responses import Response
from fastapi import Depends, APIRouter

from app.auth import get_current_user
from app.service.dependencies import get_user_service, get_token_service
from app.schemas.user import UserCreate, UserOut, LoginRequest, LoginResponse
from app.service.user import UserService
from app.service.token import TokenService

user_router = APIRouter(
    prefix="/user",
    tags=["user"]
)

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
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.log_in(str(data.email), data.password)


@user_router.post("/{user_id}/stats", status_code=200)
async def user_validation_check(
        current_user = Depends(get_current_user),
        token_service: TokenService = Depends(get_token_service)
):
    pass #await token_service.token_validation({"access_token": access_token, "refresh_token": refresh_token})

