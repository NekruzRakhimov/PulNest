from sqlalchemy.orm import Session
from db.models import AutoPayment
from db.postgres import engine
from logger.logger import logger

# Получить автоплатеж по user_id и service_id


def get_autopayment_by_user_and_service(db: Session, user_id: int, service_id: int):
    return db.query(AutoPayment).filter(AutoPayment.user_id == user_id,
                                        AutoPayment.service_id == service_id, AutoPayment.is_active == True).first()


# Записать новый автоплатеж
def create_autopayment(autopayment_data: dict):
    with Session(bind=engine) as db:
        autopayment = AutoPayment(**autopayment_data)
        db.add(autopayment)
        db.commit()
        db.refresh(autopayment)
        logger.info(f"Autopayment created for user {autopayment.user_id}, service {autopayment.service_id}, "
                    f"amount {autopayment.amount}")
        return autopayment


# Обновить автоплатеж
def update_autopayment(db: Session, autopayment_id: int, updates: dict):
    autopayment = db.query(AutoPayment).filter(AutoPayment.id == autopayment_id).first()
    if not autopayment:
        return None
    for key, value in updates.items():
        setattr(autopayment, key, value)
    db.commit()
    db.refresh(autopayment)
    logger.info(f"Autopayment {autopayment.id} updated")
    return autopayment
