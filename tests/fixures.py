import pytest
from datetime import datetime
from unittest.mock import AsyncMock

from aiogram.types import Message, User, Chat

from bot.db import Users


@pytest.fixture
def user():
    return Users(
        id=1, telegram_id=123, username="test-username", phone_number="+380991234567"
    )


@pytest.fixture
def mock_state():
    mock = AsyncMock()
    mock.update_data = AsyncMock()
    mock.set_state = AsyncMock()
    mock.get_data = AsyncMock(return_value={"username": "TestUser"})
    mock.clear = AsyncMock()
    return mock


@pytest.fixture
def mock_message():
    return Message(
        message_id=1,
        date=datetime.now(),
        chat=Chat(id=12345, type="private"),
        from_user=User(id=123, is_bot=False, first_name="TestUser"),
        text="+380991234567",
    )


@pytest.fixture
def mock_username_message():
    return Message(
        message_id=2,
        date=datetime.now(),
        chat=Chat(id=12345, type="private"),
        from_user=User(id=123, is_bot=False, first_name="TestUser"),
        text="MyTestUsername",
    )
