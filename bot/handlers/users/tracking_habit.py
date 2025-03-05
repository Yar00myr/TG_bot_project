from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from sqlalchemy.exc import SQLAlchemyError
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import select
from ...db import AsyncDB, Habits
from ...state import HabitState
from ...keyboards import get_tracking_habit_keyboard

router = Router(name=__name__)


@router.message(Command("tracking_habit"))
async def start_tracking_habit(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    keyboard = get_tracking_habit_keyboard(user_id)
    await message.answer("Виберіть опцію:", reply_markup=keyboard)
    await state.set_state(HabitState.HabitName)


@router.message(HabitState.HabitName)
async def process_habit_name(message: types.Message, state: FSMContext):
    habit_name = message.text
    await state.update_data(habit_name=habit_name)
    await message.answer(
        "Введіть частоту звички (наприклад, кількість разів на день або на тиждень):"
    )
    await state.set_state(HabitState.HabitFrequency)


@router.message(HabitState.HabitFrequency)
async def process_habit_frequency(message: types.Message, state: FSMContext):
    try:
        habit_frequency = int(message.text)
    except ValueError:
        await message.answer("Будь ласка, введіть ціле число для частоти звички.")
        return

    data = await state.get_data()
    habit_name = data.get("habit_name")
    user_id = message.from_user.id

    async with AsyncDB.get_session() as session:
        try:
            new_habit = Habits(
                user_id=user_id, habit=habit_name, frequency=habit_frequency
            )
            session.add(new_habit)
            await session.commit()
            await message.answer(
                f"Звичка '{habit_name}' успішно збережена з частотою {habit_frequency}."
            )
        except SQLAlchemyError as e:
            await session.rollback()
            await message.answer(f"Помилка при вставці в базу даних: {e}")

    await state.clear()


@router.callback_query(lambda c: c.data.startswith("view_all_habits"))
async def process_view_all_habits(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    async with AsyncDB.get_session() as session:
        habits = await session.execute(
            select(Habits.id, Habits.habit).where(Habits.user_id == user_id)
        )
        habits = habits.all()

    if habits:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=f"Видалити '{habit[1]}'",
                        callback_data=f"delete_habit_{habit[0]}",
                    ),
                    InlineKeyboardButton(
                        text=f"Оновити '{habit[1]}'",
                        callback_data=f"update_habit_{habit[0]}",
                    ),
                ]
                for habit in habits
            ]
        )
        response_text = "Ваші звички:"
        await callback_query.message.answer(response_text, reply_markup=keyboard)
    else:
        response_text = "У вас ще немає звичок."
        await callback_query.message.answer(response_text)


@router.callback_query(lambda c: c.data.startswith("delete_habit"))
async def process_delete_habit(callback_query: types.CallbackQuery):
    habit_id = int(callback_query.data.split("_")[2])
    async with AsyncDB.get_session() as session:
        try:
            habit_to_delete = await session.execute(
                select(Habits).where(Habits.id == habit_id)
            )
            habit_to_delete = habit_to_delete.scalar_one_or_none()

            if habit_to_delete:
                await session.delete(habit_to_delete)
                await session.commit()
                await callback_query.message.answer(
                    f"Звичка '{habit_to_delete.habit}' успішно видалена."
                )
            else:
                await callback_query.message.answer(
                    "Не вдалося знайти звичку для видалення."
                )
        except SQLAlchemyError as e:
            await session.rollback()
            await callback_query.message.answer(f"Помилка при видаленні звички: {e}")


@router.callback_query(lambda c: c.data.startswith("update_habit"))
async def process_update_habit(callback_query: types.CallbackQuery, state: FSMContext):
    habit_id = int(callback_query.data.split("_")[2])
    await state.update_data(habit_id=habit_id)
    await callback_query.message.answer("Введіть нову частоту для звички:")
    await state.set_state(HabitState.HabitUpdateFrequency)


@router.message(HabitState.HabitUpdateFrequency)
async def process_habit_update_frequency(message: types.Message, state: FSMContext):
    try:
        new_frequency = int(message.text)
    except ValueError:
        await message.answer("Будь ласка, введіть ціле число для частоти звички.")
        return

    data = await state.get_data()
    habit_id = data.get("habit_id")

    async with AsyncDB.get_session() as session:
        try:
            result = await session.execute(select(Habits).where(Habits.id == habit_id))
            habit_to_update = result.scalars().first()

            if habit_to_update:
                habit_to_update.frequency = new_frequency
                await session.commit()
                await message.answer(
                    f"Частота звички '{habit_to_update.habit}' успішно оновлена до {new_frequency}."
                )
            else:
                await message.answer("Не вдалося знайти звичку для оновлення.")
        except SQLAlchemyError as e:
            await session.rollback()
            await message.answer(f"Помилка при оновленні звички: {e}")

    await state.clear()


@router.callback_query(lambda c: c.data == "add_new_habit")
async def process_add_new_habit(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Введіть назву нової звички:")
    await state.set_state(HabitState.HabitName)
