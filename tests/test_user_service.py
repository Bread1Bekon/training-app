from hashlib import sha256

import pytest

from app.errors import AuthenticationError, NotFoundError
from app.schemas.user import UserCreate


@pytest.mark.asyncio
async def test_create_user_hashes_password(
    user_service, mock_user_repository, sample_user_db
):
    mock_user_repository.create_user.return_value = sample_user_db

    result = await user_service.create_user(
        UserCreate(name="Alice", email="alice@example.com", password="plain")
    )

    saved = mock_user_repository.create_user.call_args[0][0]
    assert saved["password"] == sha256(b"plain").hexdigest()
    assert result.email == "alice@example.com"


@pytest.mark.asyncio
async def test_log_in_wrong_password_raises(
    user_service, mock_user_repository, sample_user_db
):
    mock_user_repository.log_in.return_value = sample_user_db

    with pytest.raises(AuthenticationError, match="Incorrect password"):
        await user_service.log_in("alice@example.com", "wrong")


@pytest.mark.asyncio
async def test_log_in_unknown_user_raises(user_service, mock_user_repository):
    mock_user_repository.log_in.return_value = None

    with pytest.raises(NotFoundError, match="User not found"):
        await user_service.log_in("missing@example.com", "secret123")


@pytest.mark.asyncio
async def test_delete_user_not_found_raises(user_service, mock_user_repository):
    mock_user_repository.delete_user.return_value = False

    with pytest.raises(NotFoundError, match="User not found"):
        await user_service.delete_user(999)
