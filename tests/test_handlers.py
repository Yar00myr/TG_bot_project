import pytest
from datetime import datetime
from unittest.mock import AsyncMock

from aiogram.types import Message, User, Chat

from bot.db import AsyncDB, Users
from bot.handlers.users.register import register_phone
from .fixures import user_id, mock_state, mock_message


@pytest.mark.asyncio
async def test_register_phone_success(mock_message, mock_state):
    await register_phone(mock_message, mock_state)

    async with AsyncDB.get_session() as session:
        user = await session.get(Users, 123)
        assert user is not None
        assert user.username == "TestUser"
        assert user.phone_number is not None
