from aiogram.types import InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class UserCBData(CallbackData, prefix="user"):
    action: str


def users_choice() -> InlineKeyboardMarkup:
    user_choice = InlineKeyboardBuilder()
    user_choice.button(text="Гість", callback_data=UserCBData(action="guest").pack())

    user_choice.button(
        text="Реєстрація", callback_data=UserCBData(action="register").pack()
    )
    return user_choice.as_markup()
