from sqlalchemy.orm import Session
from db.models import AutoPayment
from logger.logger import logger
from pkg.repositories.autopayments import AutoPaymentRepository


# Сервисный слой с использованием абстрактного CRUD
class AutoPaymentService:
    def __init__(self, repository: AutoPaymentRepository):
        self.repository = repository

    def get_all_autopayments(self, db: Session, user_id: int):
        return self.repository.get_all(db, user_id=user_id, is_active=True)

    def get_autopayment_by_id(self, db: Session, autopayment_id: int):
        return self.repository.get_by_id(db, autopayment_id)

    def create_autopayment(self, db: Session, autopayment_data: dict):
        return self.repository.create(db, autopayment_data)

    def update_autopayment(self, db: Session, autopayment_id: int, updates: dict):
        return self.repository.update(db, autopayment_id, updates)

    def delete_autopayment(self, db: Session, autopayment_id: int):
        return self.repository.delete(db, autopayment_id)
