from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

from app.dto.user import UserDTO
from app.schemas.user import UserOut
from app.service.dependencies import get_token_service


async def get_current_user(
        credentials = Depends(HTTPBearer()),
        token_service = Depends(get_token_service),
):
    token = credentials.credentials
    user = await token_service.token_validation(token)
    if not user:
        raise HTTPException(status_code=401, detail="Token expired or invalid")
    return UserDTO.model_validate(user)