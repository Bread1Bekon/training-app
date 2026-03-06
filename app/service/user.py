from hashlib import sha256
import jwt
import datetime

from datetime import datetime, timedelta, timezone
from fastapi import HTTPException

from app.dto.user import UserDTO
from config import settings
from app.repository.token import TokenRepository
from app.repository.user import UserRepository
from app.schemas.user import UserCreate, UserOut, LoginResponse

class TokenService:
    def __init__(self, token_repository: TokenRepository):
        self.token_repository = token_repository

    async def create_access_token(self, user: UserDTO, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire, "type": "access"})
        token = jwt.encode(to_encode, settings.PRIVATE_KEY, algorithm=settings.ALGORITHM)
        await self.token_repository.add_access_token(user, token)
        return token

    async def create_refresh_token(self, user: UserDTO, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        token = jwt.encode(to_encode, settings.PRIVATE_KEY, algorithm=settings.ALGORITHM)
        await self.token_repository.add_refresh_token(user, token)
        return token

    async def token_validation(self, token: str):
        payload = await self.token_repository.check_token(token)
        if payload:
            return payload
        raise HTTPException(status_code=403, detail="Forbidden. Login failed.")

class UserService:
    def __init__(self, user_repository: UserRepository, token_service: TokenService):
        self.user_repository = user_repository
        self.token_service = token_service

    async def create_user(self, user_create: UserCreate) -> UserOut:
        user_create.password = sha256(user_create.password.encode()).hexdigest()

        user_db = await self.user_repository.create_user(user_create.model_dump())

        return UserOut.model_validate(user_db)

    async def delete_user(self, user_id: int) -> None:
        deleted = await self.user_repository.delete_user(user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="User not found")

    async def log_in(self, user_email: str, user_password: str):
        #Todo: add user data validation
        user = await self.user_repository.log_in(user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        sha256_password = sha256(user_password.encode()).hexdigest()
        if sha256_password != user.password:
            raise HTTPException(status_code=401, detail="Incorrect password")
        user_dto = UserDTO.model_validate(user)
        access_token = await self.token_service.create_access_token(user_dto, data={"sub": user.id})
        refresh_token =  await self.token_service.create_refresh_token(user_dto, data={"sub": user.id})
        response = LoginResponse(access_token=access_token, refresh_token=refresh_token)
        return LoginResponse.model_validate(response)

    async def get_user_by_id(self, user_id: int) -> UserOut:
        user = self.user_repository.get_user_by_id(user_id)
        return UserOut.model_validate(user)