import datetime
import random
import string
from datetime import datetime

from utils.email_utils import send_email
from logger.logger import logger
from utils.hash import hash_password, verify_password
from pkg.repositories import admin as admin_repository
from schemas.admin import AdminSchema
from db.models import Admin

def get_admin_by_email(email):
    admin = admin_repository.get_admin_by_email(email)
    return admin


def get_admin_by_id(admin_id):
    admin = admin_repository.get_admin_by_id(admin_id)
    return admin


def create_admin(admin: AdminSchema):
    a = Admin()
    a.name = admin.name
    a.surname = admin.surname
    a.email = admin.email
    a.password = hash_password(admin.password)
    a.role = "admin"
    a.created_at = datetime.now()

    return admin_repository.create_admin(a)


def update_admin(admin_id, admin_data: dict):
    if "password" in admin_data:
        admin_data["password"] = hash_password(admin_data["password"])
    return admin_repository.update_admin(admin_id, admin_data)


def soft_delete_admin(admin_id: int):
    return admin_repository.soft_delete_admin(admin_id)


def authenticate_admin(email: str, password: str):
    admin = admin_repository.get_admin_by_email(email)
    if not admin:
        logger.error(f"Admin not found with email: {email}")
        return None

    if not verify_password(password, admin.password):
        logger.error(f"Invalid password for admin: {email}")
        return None

    return admin