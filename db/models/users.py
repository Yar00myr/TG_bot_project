from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..models import Base
from .habits import Habits


class Users(Base):
    
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(nullable=False)
    username: Mapped[String] = mapped_column(String(50), nullable=False)
    phone_number: Mapped[int]
    
    habits: Mapped[List["Habits"]] = relationship("Habits", back_populates="user")
