from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from app.enums.user import UserType
from app.errors import AuthenticationError, NotFoundError
from app.main import app
from app.schemas.user import LoginResponse, UserOut
from app.service.dependencies import get_user_service


@pytest.fixture
def mock_user_service() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
async def client(mock_user_service: AsyncMock):
    app.dependency_overrides[get_user_service] = lambda: mock_user_service
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_register_returns_201(client, mock_user_service):
    mock_user_service.create_user.return_value = UserOut(
        id=1,
        name="Alice",
        email="alice@example.com",
        access_level=UserType.ORDINARY,
    )

    response = await client.post(
        "/user/register",
        json={
            "name": "Alice",
            "email": "alice@example.com",
            "password": "secret123",
        },
    )

    assert response.status_code == 201
    assert response.json()["email"] == "alice@example.com"


@pytest.mark.asyncio
async def test_login_wrong_password_returns_401(client, mock_user_service):
    mock_user_service.log_in.side_effect = AuthenticationError("Incorrect password")

    response = await client.post(
        "/user/login",
        json={"email": "alice@example.com", "password": "wrong"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect password"


@pytest.mark.asyncio
async def test_delete_user_not_found_returns_404(client, mock_user_service):
    mock_user_service.delete_user.side_effect = NotFoundError("User not found")

    response = await client.delete("/user/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
