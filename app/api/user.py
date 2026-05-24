from fastapi import Depends, APIRouter, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from app.api.form import form_router
from app.auth import get_current_user
from app.db import get_db
from app.models.user import UserDB
from app.dto.user import UserDTO
from app.schemas.user import UserCreate, UserOut, LoginRequest, LoginResponse
from app.schemas.user_profile import UserProfileResponse
from app.service.dependencies import get_user_service, get_form_service
from app.service.form import FormService
from app.service.user import UserService


user_router = APIRouter(
    prefix="/user",
    tags=["user"]
)
user_router.include_router(form_router)

@user_router.post("/register", response_model=UserOut, status_code=201)
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

@user_router.post("/login", response_model=LoginResponse, status_code=200)
async def log_in(
    data: LoginRequest,
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.log_in(str(data.email), data.password)


@user_router.get("/{user_id}", response_model=UserProfileResponse, status_code=200)
async def profile_info(
    user_id: int,
    current_user: UserDTO = Depends(get_current_user),
    form_service: FormService = Depends(get_form_service)
):
    form = await form_service.get_form_by_id(current_user.id)
    return UserProfileResponse(user = UserOut.model_validate(current_user), form = form)