from contextlib import asynccontextmanager
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class AsyncDB:
    ENGINE = create_async_engine("sqlite+aiosqlite:///mydb.db", echo=True)
    SESSION = async_sessionmaker(bind=ENGINE, expire_on_commit=False)

    @classmethod
    async def up(cls):
        async with cls.ENGINE.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @classmethod
    async def down(cls):
        async with cls.ENGINE.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @classmethod
    async def migrate(cls):
        async with cls.ENGINE.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    @asynccontextmanager
    async def get_session():
        async with AsyncDB.SESSION() as session:
            yield session


from .models import Habits, Reminders, Users
