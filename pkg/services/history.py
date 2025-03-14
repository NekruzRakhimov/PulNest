from pkg.repositories import history as history_repository
from schemas.history import HistoryTransaction

from logger.logger import logger



def get_transactions(user_id, min_amount, max_amount, start_date, end_date, state, tran_type, source_type, dest_type):
    transactions = history_repository.get_transactions(user_id, min_amount, max_amount, start_date, end_date, state, tran_type, source_type, dest_type)
    logger.info(f"Found {len(transactions)} transactions for user_id={user_id}")
    history = []
    for transaction in transactions:
        t = HistoryTransaction(
            id=transaction.id,
            source_type=transaction.source_type,
            source_id=transaction.source_id,
            source_number=transaction.source_number,
            amount=transaction.amount,
            dest_type=transaction.dest_type,
            dest_id=transaction.dest_id,
            dest_number=transaction.dest_number,
            status=transaction.status,
            created_at=transaction.created_at.strftime('%Y-%m-%d %H:%M:%S')
        )
        history.append(t)
    return history  






