import hashlib
import re
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReactionTypeEmoji
from sqlalchemy.exc import SQLAlchemyError
from db import Users, Session
from ...state.register import RegisterState


router = Router(name=__name__)


def hash_phone_number(phone_number: str) -> str:
    """Hash the phone number using SHA-256."""
    return hashlib.sha256(phone_number.encode("utf-8")).hexdigest()


@router.message(RegisterState.username)
async def register_name(message: Message, state: FSMContext):
    await message.answer(
        "Дякую! Тепер надішліть свій номер телефону у форматі +380XXXXXXXXX."
    )
    await state.update_data(username=message.text)
    await state.set_state(RegisterState.phone_number)


@router.message(RegisterState.phone_number)
async def register_phone(message: Message, state: FSMContext):
    """Handles the user's phone number during the registration process.

    Validates the phone number format and checks if it is already registered in the database.
    If valid and not already registered, hashes the phone number, saves the user to the database,
    and completes the registration process.

    Args:
        message (Message): The incoming message containing the user's phone number.
        state (FSMContext): The finite state machine context for the current user session.
    """
    phone_number = message.text
    if re.match(r"^\+?380\d{9}$", phone_number):
        hashed_phone_number = hash_phone_number(phone_number)
        session = Session()
        try:
            # Check if the hashed phone number already exists in the database
            existing_user = (
                session.query(Users).filter_by(phone_number=hashed_phone_number).first()
            )
            if existing_user:
                await message.answer("Цей номер телефону вже зареєстровано.")
            else:
                reg_data = await state.get_data()
                reg_name = reg_data.get("username")

                # Get the Telegram user ID
                telegram_id = message.from_user.id

                # Add the user to the database with the hashed phone number
                new_user = Users(
                    telegram_id=telegram_id,
                    username=reg_name,
                    phone_number=hashed_phone_number,
                )
                session.add(new_user)
                session.commit()
                await message.answer(
                    f"Реєстрація успішна!\nІм'я: {reg_name}\nНомер телефону: {phone_number}"
                )
                await message.react([ReactionTypeEmoji(emoji="👍")])
        except SQLAlchemyError as e:
            session.rollback()
            await message.answer(f"Помилка при вставці в базу даних: {e}")
        finally:
            await state.clear()
            session.close()
    else:
        await message.answer(
            "Номер телефону введено некоректно. Будь ласка, введіть номер у форматі +380XXXXXXXXX."
        )
