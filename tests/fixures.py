import pytest
from datetime import datetime
from unittest.mock import AsyncMock

from aiogram.types import Message, User, Chat


@pytest.fixture
def user_id():
    """Fixture for providing a mock user_id.

    This fixture is used to simulate a user ID that will be passed
    into tests for generating keyboards.

    Returns:
        int: A mock user ID (123).
    """
    return 123


@pytest.fixture
def mock_state():
    state = AsyncMock()
    state.get_data.return_value = {"username": "TestUser"}
    return state


@pytest.fixture
def mock_message():

    return Message(
        message_id=1,
        date=datetime.now(),
        chat=Chat(id=123, type="private"),
        from_user=User(id=123, is_bot=False, first_name="Test"),
        text="+380991234567",
    )
