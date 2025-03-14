from sqlalchemy.orm import Session

from db.postgres import engine
from db.models import Transactions

from logger.logger import logger




def get_transactions(user_id, min_amount, max_amount, start_date, end_date, state, tran_type, source_type, dest_type):
    logger.info(f"Getting all transactions... user_id={user_id}")

    with Session(bind=engine) as db:
        query = db.query(Transactions).filter(Transactions.user_id == user_id)

        if min_amount is not None:
            query = query.filter(Transactions.amount >= min_amount)
        if max_amount is not None:
            query = query.filter(Transactions.amount <= max_amount)
        if start_date is not None:
            query = query.filter(Transactions.created_at >= start_date)
        if end_date is not None:
            query = query.filter(Transactions.created_at <= end_date)
        if state is not None:
            query = query.filter(Transactions.status == state)
        if tran_type is not None:
            query = query.filter(Transactions.tran_type == tran_type)
        if source_type is not None:
            query = query.filter(Transactions.source_type == source_type)
        if dest_type is not None:
            query = query.filter(Transactions.dest_type == dest_type)

        return query.all()  

