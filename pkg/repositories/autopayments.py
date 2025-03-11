from sqlalchemy.orm import Session
from db.models import AutoPayment
from logger.logger import logger


# Получить все автоплатежи по user_id
def get_all_autopayments(db: Session, user_id: int):
    autopayments = db.query(AutoPayment).filter(AutoPayment.user_id == user_id, AutoPayment.is_active == True).all()

    # Добавляем merchant_name для каждого автоплатежа
    for autopayment in autopayments:
        autopayment.merchant_name = autopayment.service.merchant_name if autopayment.service else None

    return autopayments


# Получить автоплатеж по user_id и service_id
def get_autopayment_by_user_and_service(db: Session, user_id: int, service_id: int):
    autopayment = db.query(AutoPayment).filter(AutoPayment.user_id == user_id,
                                               AutoPayment.service_id == service_id,
                                               AutoPayment.is_active == True).first()

    if autopayment:
        # Добавляем merchant_name
        autopayment.merchant_name = autopayment.service.merchant_name if autopayment.service else None

    return autopayment


# Получить автоплатеж по ID
def get_autopayment_by_id(db: Session, autopayment_id: int):
    autopayment = db.query(AutoPayment).filter(AutoPayment.id == autopayment_id, AutoPayment.is_active == True).first()

    if autopayment:
        # Добавляем merchant_name
        autopayment.merchant_name = autopayment.service.merchant_name if autopayment.service else None

    return autopayment


# Записать новый автоплатеж
def create_autopayment(db: Session, autopayment_data: dict):
    autopayment = AutoPayment(**autopayment_data)

    # Убираем проверку уникальности
    db.add(autopayment)
    db.commit()
    db.refresh(autopayment)

    logger.info(f"Autopayment created for user {autopayment.user_id}, service {autopayment.service_id}, "
                f"amount {autopayment.amount}, merchant_name {autopayment.service.merchant_name if autopayment.service else 'N/A'}")
    return autopayment


# Обновить автоплатеж
def update_autopayment(db: Session, autopayment_id: int, updates: dict):
    autopayment = db.query(AutoPayment).filter(AutoPayment.id == autopayment_id).first()

    if not autopayment:
        logger.warning(f"Autopayment with ID {autopayment_id} not found.")
        return None

    for key, value in updates.items():
        setattr(autopayment, key, value)

    db.commit()
    db.refresh(autopayment)

    logger.info(f"Autopayment {autopayment.id} updated, new details: {updates}")
    return autopayment
