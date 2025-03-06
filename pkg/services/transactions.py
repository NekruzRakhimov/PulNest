from db.models import Transactions
from pkg.repositories import transactions as transactions_repository
from logger.logger import logger




def card_to_card(user_id, expense_sender, income_receiver, amount, status):
    t = Transactions(
        user_id = user_id,
        source_type = "card",
        source_id = expense_sender,
        amount = amount,
        dest_type = "card",
        dest_id = income_receiver,
        status = status
    )
    logger.info(f"Transaction: sender {expense_sender}, receiver {income_receiver}, amount {amount}, status {status}")
    transactions_repository.card_to_card(t)
    



