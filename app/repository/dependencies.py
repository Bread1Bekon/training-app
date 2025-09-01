from sqlalchemy.ext.asyncio import AsyncSession

from .user import UserRepository

def get_user_repository(db: AsyncSession):
    repository = UserRepository(db)
    return repository