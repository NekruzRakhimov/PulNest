from datetime import datetime

from logger.logger import logger
from pkg.repositories import category as category_repository
from schemas.category import CategorySchema, CategoryResponse

def create_category(category_data: CategorySchema):
    try:
        created_category = category_repository.create_category(category_data.name)
        return created_category
    except Exception as e:
        logger.error(f"Error creating category: {e}")
        raise


def get_category_by_id(category_id):
    try:
        category = category_repository.get_category_by_id(category_id)
        if category is not None:
            return category
        else:
            return None
    except Exception as e:
        logger.error(f"Error retrieving category {category_id}: {e}")
        raise


def get_all_categories():
    try:
        categories = category_repository.get_all_categories()
        logger.info(f"Retrieved {len(categories)} categories.")
        return categories
    except Exception as e:
        logger.error(f"Error retrieving all categories: {e}")
        raise


def update_category(category_id, category_data: CategorySchema):
    try:
        category = category_repository.update_category(category_id, category_data.name)
        if category is not None:
            logger.info(f"Category {category_id} updated.")
            return category
        else:
            return None
    except Exception as e:
        logger.error(f"Error updating category {category_id}: {e}")
        raise


def soft_delete_category(category_id):
    try:
        category = category_repository.soft_delete_category(category_id)
        if category:
            logger.info(f"Category {category_id} soft deleted.")
            return category
        else:
            return None
    except Exception as e:
        logger.error(f"Error soft deleting category {category_id}: {e}")
        raise