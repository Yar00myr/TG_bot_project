from aiogram.fsm.state import StatesGroup, State


class RegisterState(StatesGroup):
    """this class is a state for register"""

    username = State()
    phone_number = State()
