from unittest.mock import AsyncMock, MagicMock

import pytest

from app.dto.user import UserDTO
from app.enums.form import ModFormStatus
from app.enums.user import UserType
from app.errors import ForbiddenError
from app.service.form import FormService


@pytest.fixture
def mock_form_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_skill_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_form_producer() -> MagicMock:
    producer = MagicMock()
    producer.publish = MagicMock()
    return producer


@pytest.fixture
def form_service(
    mock_form_repository, mock_skill_repository, mock_form_producer
) -> FormService:
    return FormService(
        mock_form_repository, mock_skill_repository, mock_form_producer
    )


@pytest.fixture
def ordinary_user() -> UserDTO:
    return UserDTO(
        id=2,
        name="Bob",
        email="bob@example.com",
        password="hash",
        access_level=UserType.ORDINARY,
    )


@pytest.fixture
def moderator_user() -> UserDTO:
    return UserDTO(
        id=1,
        name="Mod",
        email="mod@example.com",
        password="hash",
        access_level=UserType.MODERATOR,
    )


@pytest.mark.asyncio
async def test_update_form_status_forbidden_for_ordinary_user(
    form_service, mock_form_repository, ordinary_user
):
    with pytest.raises(ForbiddenError):
        await form_service.update_form_status(
            1, ModFormStatus.approved, ordinary_user, None
        )

    mock_form_repository.update_form_status.assert_not_called()


@pytest.mark.asyncio
async def test_update_form_status_publishes_event_for_moderator(
    form_service, mock_form_repository, mock_form_producer, moderator_user
):
    form = MagicMock()
    form.user_id = 42
    mock_form_repository.update_form_status.return_value = form

    result = await form_service.update_form_status(
        1, ModFormStatus.approved, moderator_user, "Looks good"
    )

    mock_form_repository.update_form_status.assert_called_once_with(
        1, ModFormStatus.approved
    )
    mock_form_producer.publish.assert_called_once()
    assert result is form
