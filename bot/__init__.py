from os import getenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
from dotenv import load_dotenv

from .handlers import router as main_router
from .db import AsyncDB

load_dotenv()
TOKEN = getenv("TELEGRAM_TOKEN")

dp = Dispatcher()


async def command_error(message: Message):
    """This function is triggered when the user sends a command that is not recognized
    by the bot. It sends a response to the user indicating that the command is invalid.

    Args:
        message (Message): The incoming message containing the unrecognized command.
    """
    await message.answer(f"Команди {message.text} немає!!!")


async def start() -> None:
    """Launches the bot functionality"""
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await bot.delete_webhook(drop_pending_updates=True)

    dp.include_routers(main_router)
    await dp.start_polling(bot)
