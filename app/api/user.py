from fastapi.responses import Response
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.service.dependencies import get_user_service
from app.schemas.user_schemas import UserCreate, UserOut
from app.service.user import UserService

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