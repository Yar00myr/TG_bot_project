from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_tracking_habit_keyboard(user_id):
    row = [
        InlineKeyboardButton(
            text="Подивитися всі мої звички", callback_data=f"view_all_habits_{user_id}"
        ),
        InlineKeyboardButton(text="Додати нову звичку", callback_data="add_new_habit"),
    ]
    rows = [row]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    return markup
