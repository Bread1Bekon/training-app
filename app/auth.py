from fastapi import Depends
from fastapi.security import HTTPBearer

from app.service.token import TokenService


async def get_current_user(credentials = Depends(HTTPBearer())):
    token = credentials.credentials
    TokenService.token_validation(token)
    return credentials