from sqlalchemy.orm import Session
from db.postgres import engine
from db.models import Transactions
from logger.logger import logger



def p_2_p(t: Transactions):
    with Session(bind=engine) as db:
        transaction = Transactions(
            user_id=t.user_id,
            tran_type=t.tran_type,
            source_type=t.source_type,
            source_id=t.source_id,
            source_number=t.source_number,  
            amount=t.amount,
            dest_type=t.dest_type,
            dest_id=t.dest_id,
            dest_number=t.dest_number,  
            comment=t.comment,
            status=t.status
        )

        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        logger.info(f"After commit: source_id={transaction.source_id}, dest_id={transaction.dest_id}, amount={transaction.amount}")
        return transaction.id
        


def add_correlation_id(transaction_id, correlation_id):
    with Session(bind=engine) as db:
        logger.info(f"Adding correlation id... transaction_id={transaction_id}, correlation_id={correlation_id}")
        db_transaction = db.query(Transactions).filter(Transactions.id == transaction_id).first()
        
        if db_transaction is None:
            return None

        db_transaction.correlation_id=correlation_id
        
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction.id





