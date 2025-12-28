from sqlalchemy.ext.asyncio import AsyncSession

from .token import TokenRepository
from .user import UserRepository

def get_user_repository(db: AsyncSession):
    repository = UserRepository(db)
    return repository

def get_token_repository():
    repository = TokenRepository()
    return repository