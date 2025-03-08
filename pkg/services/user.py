import datetime
import random
import string
from datetime import datetime

from utils.email_utils import send_email 
from logger.logger import logger
from utils.hash import hash_password, verify_password
from pkg.repositories import user as user_repository
from pkg.repositories import wallet as wallet_repository
from schemas.user import UserSchema
from db.models import User


def get_user_by_phone(phone):
    user = user_repository.get_user_by_phone(phone)
    return user


def get_user_by_email(email):
    user = user_repository.get_user_by_email(email)
    return user


def get_user_by_phone_and_password(phone, password):
    user = user_repository.get_user_by_phone(phone)  # Получаем пользователя по phone

    if user is None:
        return None

    if not verify_password(password, user.password):
        logger.error(f'Invalid password: {password}')
        return None

    return user


def create_user(user: UserSchema):
    u = User()
    u.name = user.name
    u.surname = user.surname
    u.email = user.email
    u.phone = user.phone
    u.password = hash_password(user.password)
    u.role = "user"
    u.created_at = datetime.now()

    return user_repository.create_user(u)



def generate_verification_code():
     return ''.join(random.choices(string.digits, k=6))


def send_verification_email(email: str):
    code = generate_verification_code()
    user_repository.save_verification_code(email, code) 
    subject = "Your Verification Code"
    body = f"Your verification code is: {code}"
    send_email(email, subject, body)
    return code



def verify_user(email: str, user_code: str):
    db_code = user_repository.get_verification_code(email)
    if not db_code:
        return False

    if datetime.now() > db_code.expires_at:
        user_repository.delete_verification_code(email)  # Clean up expired code
        return False

    if user_code == db_code.code:
        user_repository.verify_user(email)
        user = get_user_by_email(email=email)
        wallet_repository.create_wallet(user.id, user.phone)
        user_repository.delete_verification_code(email)  # Clean up used code
        return True

    return False



