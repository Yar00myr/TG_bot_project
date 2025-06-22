import pytest

from aiogram.types import InlineKeyboardMarkup

from bot.keyboards import get_tracking_habit_keyboard, users_choice, UserCBData
from .fixures import user


def test_get_tracking_habit_keyboard(user):
    keyboard = get_tracking_habit_keyboard(user)

    assert isinstance(keyboard, InlineKeyboardMarkup)

    assert len(keyboard.inline_keyboard) == 1

    assert len(keyboard.inline_keyboard[0]) == 2

    first_button = keyboard.inline_keyboard[0][0]
    assert first_button.text == "Подивитися всі мої звички"
    assert first_button.callback_data == f"view_all_habits_{user}"

    second_button = keyboard.inline_keyboard[0][1]
    assert second_button.text == "Додати нову звичку"
    assert second_button.callback_data == "add_new_habit"


def test_users_choice():
    keyboard = users_choice()

    assert isinstance(keyboard, InlineKeyboardMarkup)

    assert len(keyboard.inline_keyboard) == 1

    assert len(keyboard.inline_keyboard[0]) == 2

    guest_button = keyboard.inline_keyboard[0][0]
    assert guest_button.text == "Гість"
    assert guest_button.callback_data == UserCBData(action="guest").pack()

    register_button = keyboard.inline_keyboard[0][1]
    assert register_button.text == "Реєстрація"
    assert register_button.callback_data == UserCBData(action="register").pack()
