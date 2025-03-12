from decimal import Decimal

from db.models import Transaction
from pkg.repositories import transactions as transactions_repository
from pkg.repositories import wallet as wallets_repository
from pkg.repositories import service as service_repository
from pkg.services import cards as cards_services
from logger.logger import logger

    

def card_to_card(user_id, expense_sender_id, sender_card_number, income_receiver_id, receiver_card_number, amount, status):
    logger.info(f"expense_sender_id={expense_sender_id}, income_receiver_id={income_receiver_id}")

    if not expense_sender_id or not income_receiver_id:
        logger.error(f"Invalid transaction: sender={expense_sender_id}, receiver={income_receiver_id}")
        return

    t = Transaction(
        user_id=user_id,
        source_type="card",
        source_id=expense_sender_id,
        source_number = (f"{sender_card_number[:4]}****{sender_card_number[-4:]}"), 
        amount=amount,
        dest_type="card",
        dest_id=income_receiver_id,
        dest_number=(f"{receiver_card_number[:4]}****{receiver_card_number[-4:]}"), 
        status=status
    )

    logger.info(f"Transaction: sender {expense_sender_id}, receiver {income_receiver_id}, amount {amount}, status {status}")
    transactions_repository.card_to_card(t)




def pay_service_by_wallet(user_id, service_id, amount, account_number, comment = None):
    try:
        service = service_repository.get_service_by_id(service_id)
        user_wallet = wallets_repository.get_wallet_by_user_id(user_id)
        user_balance = user_wallet.balance
        if service is not None:
            if user_balance < amount:
                logger.error(f"Insufficient wallet balance for user {user_id}.")
                
                transaction_data = Transaction(
                user_id = user_id,
                tran_type = "expense",
                source_type = "wallet",
                source_id = user_id,
                source_number = user_wallet.phone,
                amount = amount,
                dest_type = "service",
                dest_id = service_id,
                dest_number = account_number,
                comment = comment,
                status = "failed")
            
                transactions_repository.create_transaction(transaction_data)
            
                return -1   

            else:
                wallet_new_balance = user_wallet.balance - Decimal(amount)
                updated_wallet = wallets_repository.update_wallet_balance(user_wallet, wallet_new_balance)

                if updated_wallet:

                    service_new_balance = service_repository.update_service_balance(service_id, Decimal(amount))

                    if service_new_balance > 0:

                        # Create transaction record for user
                        transaction_data = transaction_data = Transaction(
                        user_id = user_id,
                        tran_type = "expense",
                        source_type = "wallet",
                        source_id = user_wallet.id,
                        source_number = user_wallet.phone,
                        amount = amount,
                        dest_type = "service",
                        dest_id = service_id,
                        dest_number = account_number,
                        comment = comment,
                        status = "success")

                        expense_transaction_id = transactions_repository.create_transaction(transaction_data)

                        # Create transaction record for service
                        transaction_data = transaction_data = Transaction(
                        user_id = user_id,
                        tran_type = "income",
                        source_type = "wallet",
                        source_id = user_wallet.id,
                        source_number = user_wallet.phone,
                        amount = amount,
                        dest_type = "service",
                        dest_id = service_id,
                        dest_number = account_number,
                        comment = comment,
                        status = "success")

                        income_transaction_id = transactions_repository.create_transaction(transaction_data)

                        transactions_repository.update_correlation_id(expense_transaction_id, income_transaction_id)
                        transactions_repository.update_correlation_id(income_transaction_id, expense_transaction_id)

                        return expense_transaction_id
                    
                    else:
                        wallet_new_balance = updated_wallet.balance +  Decimal(amount)
                        updated_wallet = wallets_repository.update_wallet_balance(updated_wallet, wallet_new_balance)

                        logger.error(f"Could not transfer funds to provider.")

                        transaction_data = Transaction(
                        user_id = user_id,
                        tran_type = "expense",
                        source_type = "wallet",
                        source_id = user_id,
                        source_number = user_wallet.phone,
                        amount = amount,
                        dest_type = "service",
                        dest_id = service_id,
                        dest_number = account_number,
                        comment = comment,
                        status = "failed")
                    
                        transactions_repository.create_transaction(transaction_data)
                    
                        return None
        else:
            return -2

    except Exception as e:
        logger.error(f"Error processing wallet payment: {e}")
        raise



def pay_service_by_card(user_id, service_id, amount, card_number, account_number, comment = None):
    try:
        service = service_repository.get_service_by_id(service_id)
        user_card = cards_services.get_card_by_card_number(user_id, card_number)
        user_balance = user_card.balance
        if service is not None:
            if user_balance < Decimal(amount):
                logger.error(f"Insufficient card balance for user {user_id}.")
                
                transaction_data = Transaction(
                user_id = user_id,
                tran_type = "expense",
                source_type = "card",
                source_id = user_card.id,
                source_number = user_card.card_number,
                amount = amount,
                dest_type = "service",
                dest_id = service_id,
                dest_number = account_number,
                comment = comment,
                status = "failed")
            
                transactions_repository.create_transaction(transaction_data)
            
                return -1   

            else:
                updated_card = cards_services.expense_card_balance(user_id=user_id, 
                                                                   balance=user_balance, 
                                                                   card_id=user_card.id, 
                                                                   amount=Decimal(amount))

                if updated_card:

                    service_new_balance = service_repository.update_service_balance(service_id, Decimal(amount))

                    if service_new_balance > 0:

                        # Create transaction record for user
                        transaction_data = transaction_data = Transaction(
                        user_id = user_id,
                        tran_type = "expense",
                        source_type = "card",
                        source_id = user_card.id,
                        source_number = user_card.card_number,
                        amount = amount,
                        dest_type = "service",
                        dest_id = service_id,
                        dest_number = account_number,
                        comment = comment,
                        status = "success")

                        expense_transaction_id = transactions_repository.create_transaction(transaction_data)

                        # Create transaction record for service
                        transaction_data = transaction_data = Transaction(
                        user_id = user_id,
                        tran_type = "income",
                        source_type = "card",
                        source_id = user_card.id,
                        source_number = user_card.card_number,
                        amount = amount,
                        dest_type = "service",
                        dest_id = service_id,
                        dest_number = account_number,
                        comment = comment,
                        status = "success")

                        income_transaction_id = transactions_repository.create_transaction(transaction_data)

                        transactions_repository.update_correlation_id(expense_transaction_id, income_transaction_id)
                        transactions_repository.update_correlation_id(income_transaction_id, expense_transaction_id)

                        return expense_transaction_id
                    
                    else:
                        updated_card = cards_services.income_card_balance(user_id=user_id, 
                                                                   balance=user_balance, 
                                                                   card_id=user_card.id, 
                                                                   amount=Decimal(amount))

                        logger.error(f"Could not transfer funds to provider.")

                        transaction_data = Transaction(
                        user_id = user_id,
                        tran_type = "expense",
                        source_type = "card",
                        source_id = user_card.id,
                        source_number = user_card.card_number,
                        amount = amount,
                        dest_type = "service",
                        dest_id = service_id,
                        dest_number = account_number,
                        comment = comment,
                        status = "failed")
                    
                        transactions_repository.create_transaction(transaction_data)
                    
                        return None
        else:
            return -2

    except Exception as e:
        logger.error(f"Error processing card payment: {e}")
        raise


