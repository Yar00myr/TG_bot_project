from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from db import engine


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    

def up():
    Base.metadata.create_all(engine)

def down():
    Base.metadata.drop_all(engine)


from .users import Users

from .habits import Habits

from.reminders import Reminders

down()
up()
