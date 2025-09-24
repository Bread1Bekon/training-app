from fastapi.responses import Response
from fastapi import Depends, APIRouter, Cookie
from fastapi.responses import JSONResponse

from app.service.dependencies import get_user_service
from app.schemas.user import UserCreate, UserOut
from app.service.user import UserService, token_validation

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

@user_router.post("/{user_id}", response_model=dict[str, str], status_code=200)
async def log_in(
    user_email: str,
    user_password: str,
    user_service: UserService = Depends(get_user_service)
):
    response_tokens = await user_service.log_in(user_email, user_password)
    access_token = response_tokens["access_token"]
    refresh_token = response_tokens["refresh_token"]
    return JSONResponse(
        content={"access_token": access_token, "refresh_token": refresh_token},
        status_code=200
    )

@user_router.post("/{user_id}/stats", status_code=200)
async def user_validation_check(
        access_token: str = Cookie(None, alias="access_token"),
        refresh_token: str = Cookie(None, alias="refresh_token"),
):
    tokens = {"access_token": access_token, "refresh_token": refresh_token}
    return await token_validation(tokens)
