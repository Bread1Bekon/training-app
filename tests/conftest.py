from hashlib import sha256
from unittest.mock import AsyncMock

import pytest

from app.dto.user import UserDTO
from app.enums.user import UserType
from app.models.user import UserDB
from app.service.user import TokenService, UserService


@pytest.fixture
def sample_user_db() -> UserDB:
    return UserDB(
        id=1,
        name="Alice",
        email="alice@example.com",
        password=sha256(b"secret123").hexdigest(),
        access_level=UserType.ORDINARY,
    )


@pytest.fixture
def sample_user_dto(sample_user_db: UserDB) -> UserDTO:
    return UserDTO.model_validate(sample_user_db)


@pytest.fixture
def mock_user_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_token_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def token_service(mock_token_repository: AsyncMock) -> TokenService:
    return TokenService(mock_token_repository)


@pytest.fixture
def user_service(
    mock_user_repository: AsyncMock, token_service: TokenService
) -> UserService:
    return UserService(mock_user_repository, token_service)
