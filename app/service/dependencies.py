from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .token import TokenService
from .user import UserService
from ..repository.dependencies import get_user_repository, get_token_repository
from ..db import get_db

def get_user_service(db: AsyncSession = Depends(get_db)):
    user_repository = get_user_repository(db)
    service = UserService(user_repository)
    return service

def get_token_service(db: AsyncSession = Depends(get_db)):
    token_repository = get_token_repository(db)
    service = TokenService(token_repository)
    return service