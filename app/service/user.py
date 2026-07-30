import jwt
import datetime

from datetime import datetime, timedelta, timezone

from app.dto.profile import ProfileDTO
from app.errors import AuthenticationError, ConflictError, ForbiddenError, NotFoundError
from app.dto.user import UserDTO
from app.schemas.user_profile import UserProfileResponse
from app.utils import SHA256HashService
from config import settings
from app.repository.profile import ProfileRepository
from app.repository.token import TokenRepository
from app.repository.user import UserRepository
from app.schemas.user import UserCreate, UserOut, LoginResponse, UserUpdate, PasswordChange


class TokenService:
    def __init__(self, token_repository: TokenRepository):
        self.token_repository = token_repository

    async def create_access_token(self, user: UserDTO, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire, "type": "access"})
        token = jwt.encode(
            to_encode, settings.PRIVATE_KEY, algorithm=settings.ALGORITHM
        )
        await self.token_repository.add_access_token(user, token)
        return token

    async def create_refresh_token(self, user: UserDTO, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
        to_encode.update({"exp": expire, "type": "refresh"})
        token = jwt.encode(
            to_encode, settings.PRIVATE_KEY, algorithm=settings.ALGORITHM
        )
        await self.token_repository.add_refresh_token(user, token)
        return token

    async def token_validation(self, token: str):
        payload = await self.token_repository.check_token(token)
        if payload:
            return payload
        raise ForbiddenError("Forbidden. Login failed.")


class UserService:
    def __init__(self, user_repository: UserRepository, token_service: TokenService, profile_repository: ProfileRepository, hash_service: SHA256HashService = SHA256HashService()):
        self.user_repository = user_repository
        self.token_service = token_service
        self.profile_repository = profile_repository
        self.hash_service = hash_service

    async def create_user(self, user_create: UserCreate) -> UserOut:

        existing_user = await self.user_repository.get_user_by_email(user_create.email)
        if existing_user:
            raise ConflictError("User with this email already exists")
        user_create.password = self.hash_service.hash(user_create.password)
        user_db = await self.user_repository.create_user(user_create.model_dump())
        await self.profile_repository.create_profile(user_db.id)
        return UserOut.model_validate(user_db)

    async def delete_user(self, user_id: int) -> None:
        deleted = await self.user_repository.delete_user(user_id)
        if not deleted:
            raise NotFoundError("User not found")

    async def log_in(self, user_email: str, user_password: str):
        user = await self.user_repository.log_in(user_email.lower())
        if not user:
            raise NotFoundError("User not found")
        if not self.hash_service.verify(user_password, user.password):
            raise AuthenticationError("Incorrect password")
        user_dto = UserDTO.model_validate(user)
        access_token = await self.token_service.create_access_token(
            user_dto, data={"sub": user.id}
        )
        refresh_token = await self.token_service.create_refresh_token(
            user_dto, data={"sub": user.id}
        )
        response = LoginResponse(access_token=access_token, refresh_token=refresh_token)
        return LoginResponse.model_validate(response)

    async def get_user_by_id(self, user_id: int) -> UserOut:
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return UserOut.model_validate(user)

    async def get_profile_by_user_id(self, user_id: int) -> ProfileDTO | None:
        profile = await self.profile_repository.get_profile_by_user_id(user_id)
        return ProfileDTO.model_validate(profile)

    async def update_user(self, user_id: int, current_user_id: int, update_data: UserUpdate) -> UserOut:
        if user_id != current_user_id:
            raise ForbiddenError("You can only edit your own profile")
        user = await self.user_repository.update_user(user_id, update_data.model_dump(exclude_none=True))
        if not user:
            raise NotFoundError("User not found")
        return UserOut.model_validate(user)

    async def change_password(self, user_id: int, current_user_id: int, password_data: PasswordChange) -> None:
        if user_id != current_user_id:
            raise ForbiddenError("You can only change your own password")
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        if not self.hash_service.verify(password_data.old_password, user.password):
            raise AuthenticationError("Incorrect password")
        new_hashed = self.hash_service.hash(password_data.new_password)
        await self.user_repository.change_password(user_id, new_hashed)
