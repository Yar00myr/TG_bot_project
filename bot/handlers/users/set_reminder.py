import asyncio
from aiogram import Router, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from db import AsyncDB, Habits, Reminders
from datetime import datetime, timedelta
from ...state.tracking_habit import HabitState

router = Router(name=__name__)


async def check_reminders(bot: Bot):
    while True:
        now = datetime.now().replace(second=0, microsecond=0)
        print(f"Перевірка нагадувань на {now}")

        async with AsyncDB.get_session() as session:
            reminders = await session.execute(
                select(Reminders).filter(Reminders.reminder_datetime == now)
            )
            reminders = reminders.scalars().all()
            for reminder in reminders:
                print(
                    f"Нагадування знайдено для {reminder.user_id} на {reminder.reminder_datetime}"
                )
                try:
                    await bot.send_message(
                        reminder.user_id,
                        f"🔔 Нагадування: {reminder.habit.habit}\nЧас: {reminder.reminder_datetime.strftime('%Y-%m-%d %H:%M')}",
                    )
                    await session.delete(reminder)
                    await session.commit()
                except Exception as e:
                    print(f"Помилка надсилання нагадування: {e}")
                    await session.rollback()

        await asyncio.sleep(60)


@router.message(Command("set_reminders"))
async def set_reminders(message: types.Message, state: FSMContext):
    """Обробляє команду встановлення нагадування."""
    user_id = message.from_user.id

    async with AsyncDB.get_session() as session:
        habits = await session.execute(select(Habits).where(Habits.user_id == user_id))
        habits = habits.scalars().all()

    if not habits:
        await message.answer(
            "У вас немає жодної звички. Спочатку додайте звички за допомогою команди /tracking_habit."
        )
        return

    await state.update_data(habits=[{"id": h.id, "name": h.habit} for h in habits])

    habits_text = "\n".join(
        [f"{index + 1}. {habit.habit}" for index, habit in enumerate(habits)]
    )
    await message.answer(
        "Оберіть номер звички, для якої ви хочете встановити нагадування:\n"
        + habits_text
    )
    await state.set_state(HabitState.SetReminder)


@router.message(HabitState.SetReminder)
async def process_set_reminder(message: types.Message, state: FSMContext):
    """Обробляє вибір звички для встановлення нагадування."""
    user_input = message.text.strip()

    data = await state.get_data()
    habits = data.get("habits", [])

    try:
        habit_index = int(user_input) - 1
        selected_habit = habits[habit_index]
        await state.update_data(habit_id=selected_habit["id"])

        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
        await message.answer(
            f"Введіть дату та час для нагадування (наприклад, {tomorrow}):"
        )
        await state.set_state(HabitState.HabitUpdateFrequency)
    except (ValueError, IndexError):
        await message.answer("Будь ласка, оберіть правильний номер звички.")


@router.message(HabitState.HabitUpdateFrequency)
async def process_habit_update_frequency(message: types.Message, state: FSMContext):
    """Обробляє введення дати та часу для нагадування."""
    user_input = message.text.strip()

    try:
        reminder_datetime = datetime.strptime(user_input, "%Y-%m-%d %H:%M")
    except ValueError:
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
        await message.answer(
            f"Будь ласка, введіть дату та час у правильному форматі (наприклад, {tomorrow})."
        )
        return

    data = await state.get_data()
    habit_id = data.get("habit_id")

    if not habit_id:
        await message.answer("Помилка: Не вдалося знайти звичку. Почніть заново.")
        await state.clear()
        return

    async with AsyncDB.get_session() as session:
        try:
            reminder = Reminders(
                user_id=message.from_user.id,
                habit_id=habit_id,
                reminder_datetime=reminder_datetime,
            )
            print(f"Збереження нагадування на {reminder_datetime}")
            session.add(reminder)
            await session.commit()

            
        except SQLAlchemyError as e:
            await session.rollback()
            await message.answer(f"Помилка БД: {e}")

    await state.clear()
