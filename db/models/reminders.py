import datetime
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .config import Config

Base = Config.BASE


class Reminders(Base):
    __tablename__ = "reminders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    habit_id: Mapped[int] = mapped_column(ForeignKey("users_habits.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    reminder_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    habit: Mapped["Habits"] = relationship("Habits", back_populates="reminders")
