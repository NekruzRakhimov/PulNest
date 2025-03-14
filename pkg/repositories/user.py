from sqlalchemy.orm import Session

from datetime import datetime, timedelta
from db.models import User, VerificationCode
from logger.logger import logger 
from db.postgres import engine


def create_user(user: User):
    with Session(bind=engine) as db:
        try:
            db.add(user)
            db.commit()
            logger.info(f"User created successfully with ID: {user.id}")
            return user.id
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating user: {e}")
            raise


def get_user_by_email(email):
    with Session(bind=engine) as db:
        try:
            db_user = db.query(User).filter(User.email == email).first()
            if db_user:
                logger.info(f"User found by email: {email}")
            else:
                logger.warning(f"No user found by email: {email}")
            return db_user
        except Exception as e:
            logger.error(f"Error fetching user by email {email}: {e}")
            raise


def get_user_by_phone(phone):
    with Session(bind=engine) as db:
        try:
            db_user = db.query(User).filter(User.phone == str(phone)).first()
            if db_user:
                logger.info(f"User found by phone: {phone}")
            else:
                logger.warning(f"No user found by phone: {phone}")
            return db_user
        except Exception as e:
            logger.error(f"Error fetching user by phone {phone}: {e}")
            raise


def get_user_by_phone_and_password(phone, password):
    with Session(bind=engine) as db:
        try:
            db_user = db.query(User).filter(User.phone == phone, User.password == password).first()
            if db_user:
                logger.info(f"User found by phone and password: {phone}")
            else:
                logger.warning(f"No user found by phone and password: {phone}")
            return db_user
        except Exception as e:
            logger.error(f"Error fetching user by phone {phone} and password: {e}")
            raise

def verify_user(email):
    with Session(bind=engine) as db:
        try:
            user = db.query(User).filter(User.email == email).first()
            if user:
                user.is_verified = True
                db.commit()
                logger.info(f"User {email} verified successfully.")
                return True
            else:
                logger.warning(f"User with email {email} not found.")
                return False
                   
        except Exception as e:
            db.rollback()
            logger.error(f"Error verifying user {email}: {e}")
            raise


def save_verification_code(email: str, code: str):
    with Session(bind=engine) as db:
        try:
            expires_at = datetime.now() + timedelta(minutes=20)
            user = get_user_by_email(email=email)
            if not user:
                logger.error(f"No user found for email: {email}")
                raise ValueError(f"No user found for email: {email}")
            
            verification_code = VerificationCode(user_id=user.id, email=email, code=code, expires_at=expires_at)
            db.add(verification_code)
            db.commit()
            logger.info(f"Verification code saved for email: {email}")
            return verification_code.id
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving verification code for email {email}: {e}")
            raise

def get_verification_code(email: str):
    with Session(bind=engine) as db:
        try:
            code = db.query(VerificationCode).filter(VerificationCode.email == email).first()
            if code:
                logger.info(f"Verification code found for email: {email}")
            else:
                logger.warning(f"No verification code found for email: {email}")
            return code
        except Exception as e:
            logger.error(f"Error fetching verification code for email {email}: {e}")
            raise

def delete_verification_code(email: str):
    with Session(bind=engine) as db:
        try:
            db.query(VerificationCode).filter(VerificationCode.email == email).delete()
            db.commit()
            logger.info(f"Verification code deleted for email: {email}")
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting verification code for email {email}: {e}")
            raise

