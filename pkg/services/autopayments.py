from sqlalchemy.orm import Session
from db.models import AutoPayment
from logger.logger import logger
from fastapi import HTTPException


# Получить все автоплатежи по user_id
def get_all_autopayments(db: Session, user_id: int):
    autopayments = db.query(AutoPayment).filter(AutoPayment.user_id == user_id, AutoPayment.is_active == True).all()

    # Добавляем merchant_name для каждого автоплатежа через связь с сервисом
    for autopayment in autopayments:
        autopayment.merchant_name = autopayment.service.merchant_name if autopayment.service else None

    return autopayments


# Получить автоплатеж по ID
def get_autopayment_by_id(db: Session, autopayment_id: int):
    autopayment = db.query(AutoPayment).filter(AutoPayment.id == autopayment_id, AutoPayment.is_active == True).first()

    # Добавляем merchant_name, если автоплатеж существует и связан с сервисом
    if autopayment:
        autopayment.merchant_name = autopayment.service.merchant_name if autopayment.service else None

    return autopayment


# Записать новый автоплатеж
def create_autopayment(db: Session, autopayment_data: dict):
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
        logger.warning(f"Autopayment with id {autopayment_id} not found.")
        return None

    # Обновление полей автоплатежа
    for key, value in updates.items():
        setattr(autopayment, key, value)

    db.commit()
    db.refresh(autopayment)
    logger.info(f"Autopayment {autopayment.id} updated")
    return autopayment
