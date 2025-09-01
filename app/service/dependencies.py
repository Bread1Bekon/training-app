from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .user import UserService
from ..repository.dependencies import get_user_repository
from ..db import get_db


def get_user_service(db: AsyncSession = Depends(get_db)):
    user_repository = get_user_repository(db)
    service = UserService(user_repository)
    return service