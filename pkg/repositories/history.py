from sqlalchemy.orm import Session

from db.postgres import engine
from db.models import Transactions
from logger.logger import logger
from datetime import timedelta, datetime



def get_all_transactions(user_id):
    logger.info(f"Getting all transactions... user_id={user_id}")
    with Session(bind=engine) as db:
        db_transactions = db.query(Transactions).filter(Transactions.user_id == user_id).all()
        logger.info(f"Found {len(db_transactions)} cards for user_id={user_id}")
        return db_transactions



def get_transactions_by_amount(user_id: int, min_amount, max_amount):
    logger.info(f"Getting transactions by amount range... user_id={user_id}")
    with Session(bind=engine) as db:
        db_transactions = db.query(Transactions).filter(Transactions.user_id == user_id, 
                                                Transactions.amount.between(min_amount, max_amount)).all()
        logger.info(f"Found {len(db_transactions)} cards for user_id={user_id}")
        return db_transactions



def get_transactions_by_date(user_id, start_date, end_date):
    logger.info(f"Getting transactions by date range... user_id={user_id}")

    # Преобразуем строки в datetime (если они еще не преобразованы)
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

    with Session(bind=engine) as db:
        db_transactions = (
            db.query(Transactions)
            .filter(
                Transactions.user_id == user_id,
                Transactions.created_at >= start_date,
                Transactions.created_at < end_date + timedelta(days=1)  # Учитываем конец дня
            )
            .all()
        )

        logger.info(f"Found {len(db_transactions)} transactions for user_id={user_id}")
        return db_transactions





