from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .form import FormService
from .user import UserService, TokenService
from ..elasticsearch import get_elasticsearch
from ..producers.form_producer import FormProducer
from ..repository.dependencies import (
    get_user_repository,
    get_token_repository,
    get_form_repository,
    get_skill_repository,
    get_profile_repository,
)
from ..db import get_db
from ..utils import SHA256HashService


def get_user_service(db: AsyncSession = Depends(get_db)):
    user_repository = get_user_repository(db)
    profile_repository = get_profile_repository(db)
    service = UserService(user_repository, get_token_service(), profile_repository, SHA256HashService())
    return service


def get_token_service():
    token_repository = get_token_repository()
    service = TokenService(token_repository)
    return service

def get_form_producer() -> FormProducer:
    return FormProducer()

def get_form_service(
    db: AsyncSession = Depends(get_db), elasticsearch=Depends(get_elasticsearch)
):
    form_repository = get_form_repository(db)
    skill_repository = get_skill_repository(db, elasticsearch)
    form_producer = get_form_producer()
    service = FormService(form_repository, skill_repository, form_producer)
    return service
