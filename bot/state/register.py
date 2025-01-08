from aiogram.fsm.state import StatesGroup, State


class RegisterState(StatesGroup):
    """
    this class is a state for register
    
    States:
        username (State): Represents the state where the user inputs their desired username.
        phone_number (State): Represents the state where the user provides their phone number.
    """

    username = State()
    phone_number = State()
