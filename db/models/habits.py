from typing import List
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship, mapped_column
from ..models import Base
# from .users import Users
from.reminders import Reminders


class Habits(Base):
    
    __tablename__ = "users_habits"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    habit: Mapped[str] = mapped_column(nullable=False)
    frequency: Mapped[int] = mapped_column(Integer, nullable=False)
    
    user: Mapped["Users"] = relationship("Users", back_populates="habits")
    
    reminders: Mapped[List["Reminders"]] = relationship("Reminders", back_populates="habit")
    