from aiogram.fsm.state import StatesGroup, State


class HabitState(StatesGroup):
    """
    This class is a state for habit

    States:
        HabitName (State): Represents the state where the user provides the name of the habit.
        HabitFrequency (State): Represents the state where the user sets how often the habit should occur (e.g., daily, weekly).
        HabitUpdateFrequency (State): Represents the state where the user specifies how often the habit's progress should be updated.
        SetReminder (State): Represents the state where the user sets a reminder for the habit, if applicable.
    """

    HabitName = State()
    HabitFrequency = State()
    HabitUpdateFrequency = State()
    SetReminder = State()
