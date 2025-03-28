from sqlalchemy.orm import Session

from datetime import datetime, timedelta
from db.models import Wallet
from logger.logger import logger 
from db.postgres import engine


def create_wallet(wallet):
    """
    Create a new wallet for a user.
    """
    with Session(bind=engine) as db:
        try:
            db.add(wallet)
            db.commit()
            logger.info(f"Wallet created for user {wallet.user_id}.")
            return wallet
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating wallet for user {wallet.user_id}: {e}")
            raise


def get_wallet_by_user_id(user_id):
    with Session(bind=engine) as db:
        try:
            wallet = db.query(Wallet).filter(Wallet.user_id == user_id, Wallet.deleted_at == None).first()
            if wallet:
                logger.info(f"Wallet found for user {user_id}.")
                return wallet
            else:
                logger.warning(f"No wallet found for user {user_id}.")
                return None
        except Exception as e:
            logger.error(f"Error fetching wallet for user {user_id}: {e}")
            raise


def get_wallet_by_phone(phone):
    """
    Retrieve a wallet by phone number.
    """
    with Session(bind=engine) as db:
        try:
            wallet = db.query(Wallet).filter(Wallet.phone == phone, Wallet.deleted_at == None).first()
            if wallet:
                logger.info(f"Wallet found for phone {phone}.")
                return wallet
            else:
                logger.warning(f"No wallet found for phone {phone}.")
                return None
        except Exception as e:
            logger.error(f"Error fetching wallet for phone {phone}: {e}")
            raise


def update_wallet_balance(wallet, new_balance):
    """
    Update the balance of a wallet.
    """
    with Session(bind=engine) as db:
        try:
            wallet = db.query(Wallet).filter(Wallet.id == wallet.id, Wallet.deleted_at == None).first()
            if wallet:
                wallet.balance = new_balance
                wallet.updated_at = datetime.now()
                db.commit()
                logger.info(f"Wallet {wallet.id} balance updated to {new_balance}.")
                return wallet
            else:
                logger.warning(f"No wallet found with ID {wallet.id}.")
                return None
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating balance for wallet {wallet.id}: {e}")
            raise


def update_wallet_bonus_balance(wallet, new_bonus_balance):
    """
    Update the bonus balance of a wallet.
    """
    with Session(bind=engine) as db:
        try:
            wallet = db.query(Wallet).filter(Wallet.id == wallet.id, Wallet.deleted_at == None).first()
            if wallet:
                wallet.bonus_balance = new_bonus_balance
                wallet.updated_at = datetime.now()
                db.commit()
                logger.info(f"Wallet {wallet.id} bonus balance updated to {new_bonus_balance}.")
                return wallet
            else:
                logger.warning(f"No wallet found with ID {wallet.id}.")
                return None
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating bonus balance for wallet {wallet.id}: {e}")
            raise


def soft_delete_wallet(wallet):
    """
    Soft delete a wallet by marking it as deleted.
    """
    with Session(bind=engine) as db:
        try:
            wallet = db.query(Wallet).filter(Wallet.id == wallet.id, Wallet.deleted_at == None).first()
            if wallet:
                wallet.deleted_at = datetime.now()
                db.commit()
                logger.info(f"Wallet {wallet.id} soft deleted.")
                return wallet
            else:
                logger.warning(f"No wallet found with ID {wallet.id}.")
                return None
        except Exception as e:
            db.rollback()
            logger.error(f"Error soft deleting wallet {wallet.id}: {e}")
            raise