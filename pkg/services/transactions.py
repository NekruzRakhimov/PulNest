from db.models import Transactions

from pkg.repositories import transactions as transactions_repository

from logger.logger import logger


    

def card_to_card(user_id, expense_sender_id, sender_card_number, income_receiver_id, receiver_card_number, amount, status, comment, tran_type):
    logger.info(f"expense_sender_id={expense_sender_id}, income_receiver_id={income_receiver_id}")

    if not expense_sender_id or not income_receiver_id:
        logger.error(f"Invalid transaction: sender={expense_sender_id}, receiver={income_receiver_id}")
        return

    t = Transactions(
        user_id=user_id,
        tran_type=tran_type,
        source_type="card",
        source_id=expense_sender_id,
        source_number = (f"{sender_card_number[:4]}****{sender_card_number[-4:]}"), 
        amount=amount,
        dest_type="card",
        dest_id=income_receiver_id,
        dest_number=(f"{receiver_card_number[:4]}****{receiver_card_number[-4:]}"), 
        comment=comment,
        status=status
    )

    logger.info(f"Transaction: sender {expense_sender_id}, receiver {income_receiver_id}, amount {amount}, status {status}")
    return transactions_repository.p_2_p(t)


def add_correlation_id(transaction_id, correlation_id):
    return transactions_repository.add_correlation_id(transaction_id, correlation_id )


                    
def wallet_to_wallet(user_id, expense_sender_id, sender_wallet_number, income_receiver_id, receiver_wallet_number, amount, status, comment, tran_type):
    logger.info(f"expense_sender_id={expense_sender_id}, income_receiver_id={income_receiver_id}")

    if not expense_sender_id or not income_receiver_id:
        logger.error(f"Invalid transaction: sender={expense_sender_id}, receiver={income_receiver_id}")
        return

    t = Transactions(
        user_id=user_id,
        tran_type=tran_type,
        source_type="wallet",
        source_id=expense_sender_id,
        source_number = sender_wallet_number, 
        amount=amount,
        dest_type="wallet",
        dest_id=income_receiver_id,
        dest_number=receiver_wallet_number, 
        comment=comment,
        status=status
    )

    logger.info(f"Transaction: sender {expense_sender_id}, receiver {income_receiver_id}, amount {amount}, status {status}")
    return transactions_repository.p_2_p(t)


def add_correlation_id(transaction_id, correlation_id):
    return transactions_repository.add_correlation_id(transaction_id, correlation_id )

def card_to_wallet(user_id, expense_sender_id, sender_card_number, income_receiver_id, receiver_wallet_number, amount, status, comment, tran_type):

    if not expense_sender_id or not income_receiver_id:
        logger.error(f"Invalid transaction: sender={expense_sender_id}, receiver={income_receiver_id}")
        return
    
    t = Transactions(
        user_id=user_id,
        tran_type=tran_type,
        source_type="card",
        source_id=expense_sender_id,
        source_number = (f"{sender_card_number[:4]}****{sender_card_number[-4:]}"), 
        amount=amount,
        dest_type="wallet",
        dest_id=income_receiver_id,
        dest_number=receiver_wallet_number, 
        comment=comment,
        status=status
    )

    logger.info(f"Transaction: sender {expense_sender_id}, receiver {income_receiver_id}, amount {amount}, status {status}")
    return transactions_repository.p_2_p(t)
    

def wallet_to_card(user_id, expense_sender_id, sender_wallet_number, income_receiver_id, receiver_card_number, amount, status, comment, tran_type):

    if not expense_sender_id or not income_receiver_id:
        logger.error(f"Invalid transaction: sender={expense_sender_id}, receiver={income_receiver_id}")
        return
    
    t = Transactions(
        user_id=user_id,
        tran_type=tran_type,
        source_type="wallet",
        source_id=expense_sender_id,
        source_number = sender_wallet_number, 
        amount=amount,
        dest_type="card",
        dest_id=income_receiver_id,
        dest_number=(f"{receiver_card_number[:4]}****{receiver_card_number[-4:]}"), 
        comment=comment,
        status=status
    )

    logger.info(f"Transaction: sender {expense_sender_id}, receiver {income_receiver_id}, amount {amount}, status {status}")
    return transactions_repository.p_2_p(t)