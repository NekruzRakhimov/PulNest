from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from typing import Generic, TypeVar, List, Optional
from db.models import AutoPayment
from logger.logger import logger

T = TypeVar("T")


# Абстрактный CRUD репозиторий
class AbstractCRUDRepository(ABC, Generic[T]):
    @abstractmethod
    def get_all(self, db: Session, **filters) -> List[T]:
        pass

    @abstractmethod
    def get_by_id(self, db: Session, obj_id: int) -> Optional[T]:
        pass

    @abstractmethod
    def create(self, db: Session, obj_data: dict) -> T:
        pass

    @abstractmethod
    def update(self, db: Session, obj_id: int, updates: dict) -> Optional[T]:
        pass

    @abstractmethod
    def delete(self, db: Session, obj_id: int) -> None:
        pass


# Реализация репозитория для AutoPayment
class AutoPaymentRepository(AbstractCRUDRepository[AutoPayment]):
    def get_all(self, db: Session, **filters) -> List[AutoPayment]:
        query = db.query(AutoPayment).filter_by(**filters)
        autopayments = query.all()
        for autopayment in autopayments:
            autopayment.merchant_name = autopayment.service.merchant_name if autopayment.service else None
        return autopayments

    def get_by_id(self, db: Session, obj_id: int) -> Optional[AutoPayment]:
        autopayment = db.query(AutoPayment).filter(AutoPayment.id == obj_id, AutoPayment.is_active == True).first()
        if autopayment:
            autopayment.merchant_name = autopayment.service.merchant_name if autopayment.service else None
        return autopayment

    def create(self, db: Session, obj_data: dict) -> AutoPayment:
        autopayment = AutoPayment(**obj_data)
        db.add(autopayment)
        db.commit()
        db.refresh(autopayment)
        logger.info(f"Autopayment created for user {autopayment.user_id}")
        return autopayment

    def update(self, db: Session, obj_id: int, updates: dict) -> Optional[AutoPayment]:
        autopayment = self.get_by_id(db, obj_id)
        if not autopayment:
            logger.warning(f"Autopayment with ID {obj_id} not found.")
            return None

        for key, value in updates.items():
            setattr(autopayment, key, value)

        db.commit()
        db.refresh(autopayment)
        logger.info(f"Autopayment {autopayment.id} updated.")
        return autopayment

    def delete(self, db: Session, obj_id: int) -> None:
        autopayment = self.get_by_id(db, obj_id)
        if autopayment:
            db.delete(autopayment)
            db.commit()
            logger.info(f"Autopayment {obj_id} deleted.")
