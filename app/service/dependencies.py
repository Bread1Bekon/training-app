from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .form import FormService
from .user import UserService, TokenService
from ..repository.dependencies import get_user_repository, get_token_repository, get_form_repository, \
    get_skill_repository
from ..db import get_db


def get_user_service(db: AsyncSession = Depends(get_db)):
    user_repository = get_user_repository(db)
    service = UserService(user_repository, get_token_service())
    return service

def get_token_service():
    token_repository = get_token_repository()
    service = TokenService(token_repository)
    return service

def get_form_service(db: AsyncSession = Depends(get_db)):
    form_repository = get_form_repository(db)
    skill_repository = get_skill_repository(db)
    service = FormService(form_repository, skill_repository)
    return service