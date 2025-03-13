from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from db.models import Admin, VerificationCode
from logger.logger import logger
from db.postgres import engine

def create_admin(admin: Admin):
    with Session(bind=engine) as db:
        try:
            db.add(admin)
            db.commit()
            logger.info(f"Admin created successfully with ID: {admin.id}")
            return admin.id
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating admin: {e}")
            raise


def get_admin_by_email(email):
    with Session(bind=engine) as db:
        try:
            db_admin = db.query(Admin).filter(Admin.email == email, Admin.deleted_at == None).first()
            if db_admin:
                logger.info(f"Admin found by email: {email}")
            else:
                logger.warning(f"No admin found by email: {email}")
            return db_admin
        except Exception as e:
            logger.error(f"Error fetching admin by email {email}: {e}")
            raise


def get_admin_by_id(admin_id):
    with Session(bind=engine) as db:
        try:
            db_admin = db.query(Admin).filter(Admin.id == admin_id, Admin.deleted_at == None).first()
            if db_admin:
                logger.info(f"Admin found by ID: {admin_id}")
            else:
                logger.warning(f"No admin found by ID: {admin_id}")
            return db_admin
        except Exception as e:
            logger.error(f"Error fetching admin by ID {admin_id}: {e}")
            raise


def soft_delete_admin(admin_id):
    with Session(bind=engine) as db:
        try:
            admin = db.query(Admin).filter(Admin.id == admin_id, Admin.deleted_at == None).first()
            if admin:
                admin.deleted_at = datetime.now()
                db.commit()
                logger.info(f"Admin {admin_id} soft deleted successfully.")
                return admin
            else:
                logger.warning(f"No admin found with ID {admin_id}.")
                return None
        except Exception as e:
            db.rollback()
            logger.error(f"Error soft deleting admin {admin_id}: {e}")
            raise