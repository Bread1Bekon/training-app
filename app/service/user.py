import jwt
import datetime
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from fastapi import HTTPException, status
from app.repository.user import UserRepository
from app.schemas.user import UserCreate, UserOut

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, os.getenv("PRIVATE_KEY"), algorithm="HS256")

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, os.getenv("PRIVATE_KEY"), algorithm="HS256")

def token_validation(tokens: dict):
    refresh_token = tokens.get("refresh_token")
    access_token = tokens.get("access_token")
    # Пользователь никогда не регистрировался
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please log in or register first"
        )
    decoded_refresh_token = jwt.decode(refresh_token, os.getenv("PUBLIC_KEY"), algorithms=["HS256"])
    # Пользователь регистрировался более 7 дней назад
    if decoded_refresh_token.get("exp") < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token's expiry time is invalid, please log in again"
        )
    decoded_access_token = jwt.decode(access_token, os.getenv("PUBLIC_KEY"), algorithms=["HS256"])
    # Пользователь регистрировался более 30 минут но менее 7 дней назад
    if decoded_access_token.get("exp") < datetime.now(timezone.utc):
        # Попробовать обновить токен с помощью refresh_token
        new_access_token = create_access_token(data={"sub": decoded_access_token["sub"]})
        new_refresh_token = create_refresh_token(data={"sub": decoded_refresh_token["sub"]})
        # TODO: Write a function to revoke old access token
        return {
            "status": "tokens_refreshed",
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "user_id": decoded_access_token["sub"]
        }

    # Оба токена валидны
    return {
        "status": "tokens_valid",
        "user_id": decoded_access_token["sub"],
        "message": "Tokens are valid"
    }


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, user_create: UserCreate) -> UserOut:
        user_create.password = sha256(user_create.password.encode()).hexdigest()
        user_db = await self.user_repository.create_user(user_create.model_dump())
        return UserOut.model_validate(user_db)

    async def delete_user(self, user_id: int) -> None:
        deleted = await self.user_repository.delete_user(user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="User not found")

    async def log_in(self, user_email: str, user_password: str):
        load_dotenv()
        #Todo: add user data validation
        user = await self.user_repository.log_in(user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        sha256_password = sha256(user_password.encode()).hexdigest()
        if sha256_password != user.hashed_password:
            raise HTTPException(status_code=401, detail="Incorrect password")
        access_token = create_access_token(data={"sub": user.id})
        refresh_token = create_refresh_token(data={"sub": user.id})
        return {"access_token": access_token, "refresh_token": refresh_token}
