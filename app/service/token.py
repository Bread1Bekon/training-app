import jwt
import datetime
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from jose import JWTError, ExpiredSignatureError

from app.repository.token import TokenRepository
from config import Settings

class TokenService:
    def __init__(self, user_repository: TokenRepository):
        self.user_repository = user_repository

    def create_access_token(data: dict):
        settings = Settings()
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire, "type": "access"})
        return jwt.encode(to_encode, settings.PRIVATE_KEY, algorithm=settings.ALGORITHM)

    def create_refresh_token(data: dict):
        settings = Settings()
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        return jwt.encode(to_encode, settings.PRIVATE_KEY, algorithm=settings.ALGORITHM)

    def token_validation(self, token: str):
        settings = Settings()
        access_token = token

        # Проверка наличия токенов
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Please log in or register first"
            )

        try:
            decoded_access_token = jwt.decode(access_token, Settings.PUBLIC_KEY, algorithms=[settings.ALGORITHM])
            decoded_refresh_token = jwt.decode(refresh_token, Settings.PUBLIC_KEY, algorithms=[settings.ALGORITHM])
            # Проверка срока действия access token
            # TODO: make get_current_date for universal time
            current_timestamp = datetime.now(timezone.utc).timestamp()

            if decoded_access_token.get("exp") < current_timestamp:
                # Access token истек, проверяем refresh token
                if decoded_refresh_token.get("exp") < current_timestamp:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Token's expiry time is invalid, please log in again"
                    )

                # Обновляем токены
                new_access_token = TokenService.create_access_token(data={"sub": decoded_access_token["sub"]})
                new_refresh_token = TokenService.create_refresh_token(data={"sub": decoded_refresh_token["sub"]})

                self.user_repository.revoke_token(refresh_token=refresh_token)

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

        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired, please log in again"
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )