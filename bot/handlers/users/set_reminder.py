# from aiogram import Router, types
# from aiogram.filters import Command
# from aiogram.fsm.context import FSMContext
# from datetime import datetime, timedelta
# from sqlalchemy.exc import SQLAlchemyError
# from db import Session
# from db.models.habits import Habits, Reminders
# from ...state.tracking_habit import HabitState

# router = Router(name=__name__)

# # Функція для створення нагадування
# @router.message(Command('set_reminders'))
# async def set_reminders(message: types.Message, state: FSMContext):
#     user_id = message.from_user.id
    
#     session = Session()
#     habits = session.query(Habits).filter(Habits.user_id == user_id).all()
#     session.close()
    
#     if habits:
#         habits_text = "\n".join([f"{index + 1}. {habit.habit}" for index, habit in enumerate(habits)])
#         await message.answer("Оберіть звичку, для якої ви хочете встановити нагадування:\n" + habits_text)
#         await state.set_state(HabitState.SetReminder)
#     else:
#         await message.answer("У вас немає жодної звички. Спочатку додайте звички за допомогою команди /tracking_habit.")

# @router.message(HabitState.SetReminder)
# async def process_set_reminder(message: types.Message, state: FSMContext):
#     user_input = message.text.strip()
#     session = Session()
#     habits = session.query(Habits).filter(Habits.user_id == message.from_user.id).all()
    
#     try:
#         habit_index = int(user_input) - 1
#         selected_habit = habits[habit_index]
#         await state.update_data(habit_id=selected_habit.id)
#         await message.answer("Введіть дату та час для нагадування звички (наприклад, 2024-09-15 14:00):")
#         await state.set_state(HabitState.HabitUpdateFrequency)
#     except (ValueError, IndexError):
#         await message.answer("Будь ласка, оберіть правильний номер звички.")
#         return
#     finally:
#         session.close()

# @router.message(HabitState.HabitUpdateFrequency)
# async def process_habit_update_frequency(message: types.Message, state: FSMContext):
#     user_input = message.text.strip()
    
#     try:
#         reminder_datetime = datetime.strptime(user_input, '%Y-%m-%d %H:%M')
#     except ValueError:
#         # Отримуємо завтрашню дату
#         tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
#         await message.answer(f"Введіть дату та час у валідному форматі (наприклад, {tomorrow} 14:00).")
#         return
    
#     data = await state.get_data()
#     habit_id = data.get('habit_id')
    
#     session = Session()
#     try:
#         reminder = Reminders(
#             user_id=message.from_user.id,
#             habit_id=habit_id,
#             reminder_datetime=reminder_datetime
#         )
#         session.add(reminder)
#         session.commit()
#         await message.answer(f"Нагадування для звички встановлено на {reminder_datetime.strftime('%Y-%m-%d %H:%M')}.")
#     except SQLAlchemyError as e:
#         session.rollback()
#         await message.answer(f"Помилка при встановленні нагадування: {e}")
#     finally:
#         session.close()
#         await state.clear()
    