from fastapi import Depends
from fastapi.security import HTTPBearer

from app.service.dependencies import get_token_service
from app.service.user import TokenService


async def get_current_user(credentials = Depends(HTTPBearer()), token_service = Depends(get_token_service)):
    token = credentials.credentials
    token_service.token_validation(token)
    return credentials