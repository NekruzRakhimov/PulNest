from sqlalchemy.orm import Session
from db.models import Transaction
from db.postgres import engine
from logger.logger import logger


def get_transactions(user_id, min_amount, max_amount, start_date, end_date, state, tran_type, source_type, dest_type):
    logger.info(f"Getting transactions for user_id={user_id} with filters...")

    with Session(bind=engine) as db:
        query = db.query(Transaction).filter(Transaction.user_id == user_id)

        if min_amount is not None:
            query = query.filter(Transaction.amount >= min_amount)
        if max_amount is not None:
            query = query.filter(Transaction.amount <= max_amount)
        if start_date is not None:
            query = query.filter(Transaction.created_at >= start_date)
        if end_date is not None:
            query = query.filter(Transaction.created_at <= end_date)
        if state is not None:
            query = query.filter(Transaction.status == state)
        if tran_type is not None:
            query = query.filter(Transaction.tran_type == tran_type)
        if source_type is not None:
            query = query.filter(Transaction.source_type == source_type)
        if dest_type is not None:
            query = query.filter(Transaction.dest_type == dest_type)

        return query.all()
