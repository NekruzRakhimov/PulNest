from datetime import datetime


from logger.logger import logger
from pkg.repositories import wallet as wallet_repository
from schemas import wallet as wallet_schema
from db.models import Wallet


def get_wallet_by_phone(phone_number):
    try:
        wallet = wallet_repository.get_wallet_by_phone(phone_number)
        if wallet:
            logger.info(f"Wallet retrieved with phone {phone_number}.")
            return wallet
        else:
            logger.warning(f"No wallet found with phone {phone_number}.")
            return None
    except Exception as e:
        logger.error(f"Error retrieving wallet details with phone {phone_number}: {e}")
        raise


def get_wallet_phone_number(user_id):
    try:
        # Fetch the wallet by user ID
        wallet = wallet_repository.get_wallet_by_user_id(user_id)
        if wallet:
            logger.info(f"Wallet retrieved for user {user_id}.")
            phone_number = wallet.phone
            return phone_number 
        else:
            logger.warning(f"No wallet found for user {user_id}.")
            return            
    except Exception as e:
        logger.error(f"Error retrieving wallet phone number for user {user_id}: {e}")
  


def get_wallet_balance(user_id):
    try:
        # Fetch the wallet by user ID
        wallet = wallet_repository.get_wallet_by_user_id(user_id)
        if wallet:
            logger.info(f"Wallet balance retrieved for user {user_id}.")
            return float(wallet.balance) 
        else:
            logger.warning(f"No wallet found for user {user_id}.")
            return            
    except Exception as e:
        logger.error(f"Error retrieving wallet balance for user {user_id}: {e}")


def soft_delete_wallet(user_id):
    try:
        wallet = wallet_repository.get_wallet_by_user_id(user_id)
        if wallet:
            wallet.deleted_at = datetime.now()
            wallet_repository.soft_delete_wallet(wallet)
            logger.info(f"Wallet soft deleted for user {user_id}.")
            return wallet
        else:
            logger.warning(f"No wallet found for user {user_id}.")
            return None
    except Exception as e:
        logger.error(f"Error soft deleting wallet for user {user_id}: {e}")
        raise


def wallet_topup(user_id, amount):
    try:
        wallet = wallet_repository.get_wallet_by_user_id(user_id)
        if wallet:
            if amount > 0:
                new_balance = wallet.balance + amount
                wallet_repository.update_wallet_balance(wallet, new_balance)
                wallet.updated_at = datetime.now()
                logger.info(f"Added {amount} to wallet balance for user {user_id}.")
                return True
            else:
                logger.warning(f"Amount cannot be negative.")
                return None 
        else:
            logger.warning(f"No wallet found for user {user_id}.")
            return None
    except Exception as e:
        logger.error(f"Error adding funds to wallet for user {user_id}: {e}")
        raise
        

def wallet_withdrawal(user_id, amount):
    try:
        wallet = wallet_repository.get_wallet_by_user_id(user_id)
        if wallet:
            if amount > 0:
                if wallet.balance >= amount:
                    new_balance = wallet.balance - amount
                    wallet_repository.update_wallet_balance(wallet, new_balance)
                    wallet.updated_at = datetime.now()
                    logger.info(f"Deducted {amount} from wallet balance for user {user_id}.")
                    return True
                else:
                    logger.warning(f"Insufficient balance in wallet for user {user_id}.")
                    raise ValueError("Insufficient balance")
            else:
                logger.warning(f"Amount cannot be negative.")
                return None 
        else:
            logger.warning(f"No wallet found for user {user_id}.")
            return None
    except Exception as e:
        logger.error(f"Error deducting funds from wallet for user {user_id}: {e}")
        raise


def transfer_from_wallet_to_wallet(sender_user_id, receiver_user_id, amount):
    try:
        sender_wallet = wallet_repository.get_wallet_by_user_id(sender_user_id)
        receiver_wallet = wallet_repository.get_wallet_by_user_id(receiver_user_id)

        if not sender_wallet or not receiver_wallet:
            logger.warning("Sender or receiver wallet not found.")
            raise ValueError("Sender or receiver wallet not found")

        withdrawal_status = wallet_withdrawal(sender_wallet.user_id, amount)
        
        if withdrawal_status:
            wallet_topup(receiver_wallet.user_id, amount)
            logger.info(f"Transferred {amount} from user {sender_user_id} to user {receiver_user_id}.")
            return True
        else:
            logger.warning("Funds are not transferred.")
            return None
        
    except Exception as e:
        logger.error(f"Error transferring funds: {e}")
        raise


def bonus_topup(user_id, amount):
    try:
        wallet = wallet_repository.get_wallet_by_user_id(user_id)
        if wallet:
            if amount > 0:
                new_balance = wallet.bonus_balance + amount
                wallet_repository.update_wallet_bonus_balance(wallet, new_balance)
                wallet.updated_at = datetime.now()
                logger.info(f"Added {amount} to wallet bonus balance for user {user_id}.")
                return True
            else:
                logger.warning(f"Amount cannot be negative.")
                return None 
        else:
            logger.warning(f"No wallet found for user {user_id}.")
            return None
    except Exception as e:
        logger.error(f"Error adding funds to wallet for user {user_id}: {e}")
        raise
        

def bonus_withdrawal(user_id, amount):
    try:
        wallet = wallet_repository.get_wallet_by_user_id(user_id)
        if wallet:
            if amount > 0:
                if wallet.bonus_balance >= amount:
                    new_balance = wallet.balance - amount
                    wallet_repository.update_wallet_bonus_balance(wallet, new_balance)
                    wallet.updated_at = datetime.now()
                    logger.info(f"Deducted {amount} from wallet bonus balance for user {user_id}.")
                    return True
                else:
                    logger.warning(f"Insufficient balance in wallet bonus for user {user_id}.")
                    raise ValueError("Insufficient balance")
            else:
                logger.warning(f"Amount cannot be negative.")
                return None 
        else:
            logger.warning(f"No wallet found for user {user_id}.")
            return None
    except Exception as e:
        logger.error(f"Error deducting funds from wallet for user {user_id}: {e}")
        raise