from pkg.repositories import history as history_repository
from logger.logger import logger

from schemas.history import HistoryTransaction
from datetime import datetime



def get_all_transactions(user_id: int):
    transactions = history_repository.get_all_transactions(user_id)
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



def get_transactions_by_amount(user_id: int, min_amount, max_amount):
    transactions = history_repository.get_transactions_by_amount(user_id, min_amount, max_amount)
    logger.info(f"Found by amount range{len(transactions)} transactions for user_id={user_id}")
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



def get_transactions_by_date(user_id, start_date, end_date):
    transactions = history_repository.get_transactions_by_date(user_id, start_date, end_date)
    logger.info(f"Found by date range{len(transactions)} transactions for user_id={user_id}")
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








