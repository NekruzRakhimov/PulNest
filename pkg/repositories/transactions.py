from sqlalchemy.orm import Session
from datetime import datetime

from db.postgres import engine
from db.models import Transaction
from logger.logger import logger


def p_2_p(t: Transactions):
    with Session(bind=engine) as db:
        transaction = Transaction(
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


def create_transaction(transaction_data: Transaction):
    with Session(bind=engine) as db:
        try:
            transaction = Transaction(
                user_id=transaction_data.user_id,
                tran_type=transaction_data.tran_type,
                source_type=transaction_data.source_type,
                source_id=transaction_data.source_id,
                source_number=transaction_data.source_number,
                amount=transaction_data.amount,
                dest_type=transaction_data.dest_type,
                dest_id=transaction_data.dest_id,
                dest_number=transaction_data.dest_number,
                comment=transaction_data.comment,
                correlation_id=transaction_data.correlation_id,
                status=transaction_data.status,
                created_at=datetime.now()
            )
            db.add(transaction)
            db.commit()
            logger.info(f"Transaction created in DB.")
            return transaction.id
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating transaction: {e} in DB")
            raise

            
def update_correlation_id(transaction_id, correlation_id):
    with Session(bind=engine) as db:
        try:
            transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
            
            if not transaction:
                logger.error(f"Transaction with ID {transaction_id} not found.")
                return None
            
            transaction.correlation_id = correlation_id
            
            db.commit()
            logger.info(f"Correlation ID updated for transaction ID {transaction_id}.")
            
            return transaction.id
        
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating correlation ID for transaction ID {transaction_id}: {e}")
            raise
