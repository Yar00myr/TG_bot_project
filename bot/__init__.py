from os import getenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message

# from .handlers.users.set_reminder import on_startup
from dotenv import load_dotenv

from .handlers.users import router as main_router

load_dotenv()
TOKEN = getenv("TELEGRAM_TOKEN")

dp = Dispatcher()


async def command_error(message: Message):
    await message.answer(f"Команди {message.text} немає!!!")


async def start() -> None:
    """launches the bot functionality"""
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_routers(main_router)
    await dp.start_polling(bot)
