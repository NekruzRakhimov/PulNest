from sqlalchemy.orm import Session
from datetime import datetime

from db.models import Category
from db.postgres import engine
from logger.logger import logger


def create_category(name):
    with Session(bind=engine) as db:
        try:
            category = Category(
                name=name,
                created_at=datetime.now()
            )
            db.add(category)
            db.commit()
            logger.info(f"Category created in DB.")
            return category
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating category: {e} in DB")
            raise


def get_category_by_id(category_id):
    with Session(bind=engine) as db:
        try:
            category = db.query(Category).filter(Category.id == category_id, Category.deleted_at == None).first()
            if category:
                logger.info(f"Category {category_id} retrieved from DB.")
                return category
            else:
                logger.warning(f"No category found with ID {category_id} in DB.")
                return None
        except Exception as e:
            logger.error(f"Error retrieving category {category_id}: {e} from DB")
            raise


def get_all_categories():
    with Session(bind=engine) as db:
        try:
            categories = db.query(Category).filter(Category.deleted_at == None).all()
            return categories
        except Exception as e:
            logger.error(f"Error retrieving all categories from DB: {e}")
            raise


def update_category(category_id, name):
    with Session(bind=engine) as db:
        try:
            category = db.query(Category).filter(Category.id == category_id, Category.deleted_at == None).first()
            if category is not None:
                category.name = name
                db.commit()
                logger.info(f"Category {category_id} updated.")
                return category
            else:
                logger.warning(f"No category found with ID {category_id} in DB.")
                return None
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating category {category_id}: {e} in DB")
            raise


def soft_delete_category(category_id):
    with Session(bind=engine) as db:
        try:
            category = db.query(Category).filter(Category.id == category_id, Category.deleted_at == None).first()
            if category:
                category.deleted_at = datetime.now()
                db.commit()
                logger.info(f"Category {category_id} soft deleted in DB.")
                return category
            else:
                logger.warning(f"No category found with ID {category_id} in DB.")
                return None
        except Exception as e:
            db.rollback()
            logger.error(f"Error soft deleting category {category_id}: {e} in DB")
            raise