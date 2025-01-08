from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router(name=__name__)


@router.message(Command("help"))
async def command_help_handler(message: Message):
    """
    Handles the /help command and provides information or assistance.

    This function sends a message to the user with additional contact information
    for further help or inquiries. It also adds a button for starting a new command
    for better user interaction.

    Args:
        message (Message): The message object that triggered this handler.

    Sends:
        A text message with help instructions and a keyboard button for quick actions.
    """

    if message.text.startswith("/help"):
        await message.answer(
            "Якщо вам потрібна додаткова інформація або ви маєте питання, будь ласка, зверніться за електронною поштою за адресою ivanucaromir@gmail.com"
        )
        return
