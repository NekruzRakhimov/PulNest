from sqlalchemy.orm import Session
from db.postgres import engine
from db.models import Transactions
from logger.logger import logger



def card_to_card(t: Transactions):
    with Session(bind=engine) as db:
        transaction = Transactions(
        user_id=t.user_id,
        source_type=t.source_type,
        source_id=t.source_id,  
        amount=t.amount,
        dest_type=t.dest_type,
        dest_id=t.dest_id,  
        status=t.status
        )


        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        logger.info(f"After commit: source_id={transaction.source_id}, dest_id={transaction.dest_id}, amount={transaction.amount}")
