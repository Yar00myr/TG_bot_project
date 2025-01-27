from contextlib import contextmanager
from .models import Config, Habits, Reminders, Users


def up():
    Config.BASE.metadata.create_all(Config.ENGINE)


def down():
    Config.BASE.metadata.drop_all(Config.ENGINE)


def migrate():
    down()
    up()



@contextmanager
def get_session():
    with Config.SESSION.begin() as session:
        yield session
