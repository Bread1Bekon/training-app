from sqlalchemy.ext.asyncio import AsyncSession

from .form import FormRepository, SkillRepository
from .token import TokenRepository
from .user import UserRepository

def get_user_repository(db: AsyncSession):
    repository = UserRepository(db)
    return repository

def get_token_repository():
    repository = TokenRepository()
    return repository

def get_form_repository(db: AsyncSession):
    repository = FormRepository(db)
    return repository

def get_skill_repository(db: AsyncSession):
    repository = SkillRepository(db)
    return repository