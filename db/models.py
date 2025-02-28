import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime

from db.postgres import engine


class Base(DeclarativeBase):
    pass


def migrate_tables():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Ошибка во время миграции: {e}")
