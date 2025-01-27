from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


class Config:
    ENGINE = create_engine("sqlite:///mydb.db", echo=True)
    SESSION = sessionmaker(ENGINE)
    BASE = declarative_base()
