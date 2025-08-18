from fastapi import APIRouter
from .user import user_router

root_router = APIRouter(
    prefix="",
)

root_router.include_router(user_router)