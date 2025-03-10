from db.models import Transactions
from pkg.repositories import transactions as transactions_repository
from logger.logger import logger

    

def card_to_card(user_id, expense_sender_id, sender_card_number, income_receiver_id, receiver_card_number, amount, status):
    logger.info(f"expense_sender_id={expense_sender_id}, income_receiver_id={income_receiver_id}")

    if not expense_sender_id or not income_receiver_id:
        logger.error(f"Invalid transaction: sender={expense_sender_id}, receiver={income_receiver_id}")
        return

    t = Transactions(
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


