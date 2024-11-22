from aiogram.fsm.state import StatesGroup, State


class HabitState(StatesGroup):
    """this class is a state for habit"""

    HabitName = State()
    HabitFrequency = State()
    HabitUpdateFrequency = State()
    SetReminder = State()
