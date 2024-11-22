from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router(name=__name__)


@router.message(Command("help"))
async def command_help_handler(message: Message):
    if message.text.startswith("/help"):
        await message.answer(
            "Якщо вам потрібна додаткова інформація або ви маєте питання, будь ласка, зверніться за електронною поштою за адресою ivanucaromir@gmail.com"
        )
        return
