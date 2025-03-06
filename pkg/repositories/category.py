from typing import List, Type

from sqlalchemy.orm import Session
from db.postgres import engine
from db.models import Category
from logger.logger import logger
import datetime


def get_categories() -> list[Type[Category]]:
    with Session(engine) as session:
        return session.query(Category).all()


def get_category_by_id(category_id: int) -> Type[Category]:
    with Session(engine) as session:
        return session.query(Category).filter_by(id=category_id).first()


def get_category_by_name(category_name: str) -> Type[Category]:
    with Session(engine) as session:
        return session.query(Category).filter_by(name=category_name).first()


def create_new_category(category_name: str) -> Category:
    with Session(engine) as session:
        new_category = Category(
            category_name=category_name,
        )

        session.add(new_category)
        session.commit()
        return new_category


def update_category_by_id(category_id: int, category_name: str) -> Type[Category] | None:
    with Session(engine) as session:
        category = session.query(Category).filter_by(id=category_id).first()
        category.category_name = category_name
        session.commit()
        return category


def delete_category_by_id(category_id: int) -> None:
    with Session(engine) as session:
        category = session.query(Category).filter_by(id=category_id).first()
        session.delete(category)
        session.commit()
        return

