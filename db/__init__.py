from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///my.sql", echo=True)
Session = sessionmaker(engine)


from .models import Base, Users, Habits, Reminders
