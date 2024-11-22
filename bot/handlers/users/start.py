from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from ...state.register import RegisterState
from ...keyboards.user_choice import users_choice, UserCBData


router = Router(name=__name__)


@router.message(CommandStart())
async def start_register(message: Message):
    await message.answer(
        "Привіт. Для продовження виберіть як ви хочите зайти?",
        reply_markup=users_choice(),
    )


@router.callback_query(UserCBData.filter())
async def handle_user_choice(
    callback_query: CallbackQuery, callback_data: UserCBData, state: FSMContext
):
    if callback_data.action == "register":
        await callback_query.message.answer(
            "Для реєстрації, будь ласка, введіть своє ім'я."
        )
        await state.set_state(RegisterState.username)
    elif callback_data.action == "guest":
        await callback_query.message.answer("Ви обрали режим гостя.")
    await callback_query.answer()
