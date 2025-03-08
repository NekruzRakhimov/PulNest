from logger.logger import logger
from pkg.repositories import wallet as wallet_repository
from schemas import wallet as wallet_schema
from db.models import Wallet

def get_wallet_balance(user_id: int):
    try:
        # Fetch the wallet by user ID
        wallet = wallet_repository.get_wallet_by_user_id(user_id)
        if wallet:
            logger.info(f"Wallet balance retrieved for user {user_id}.")
            return float(wallet.balance)  # Convert Decimal to float
        else:
            logger.warning(f"No wallet found for user {user_id}.")
            return            
    except Exception as e:
        logger.error(f"Error retrieving wallet balance for user {user_id}: {e}")
        