from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from schemas.autopayments import AutoPaymentCreate, AutoPaymentOut, AutoPaymentUpdate
from pkg.services import autopayments as a_service
from db.postgres import engine  # Импорт движка для создания сессии

router = APIRouter()


# Функция для получения сессии
def get_db_session():
    return Session(bind=engine)


# Создание автоплатежа
@router.post("/autopayment", response_model=AutoPaymentOut, tags=["autopayments"])
def create_autopayment(autopayment: AutoPaymentCreate):
    db = get_db_session()  # Создаем сессию вручную
    try:
        autopayment_data = {
            "user_id": autopayment.user_id,
            "amount": autopayment.amount,
            "service_id": autopayment.service_id,
            "title": autopayment.title
        }
        result = a_service.create_autopayment(db=db, autopayment_data=autopayment_data)
        if not result:
            raise HTTPException(status_code=400, detail="Failed to create autopayment")

        # Формируем ответ в нужном формате
        return {
            "title": result.title,
            "amount": result.amount,
            "payment_date": result.payment_date
        }
    finally:
        db.close()  # Закрываем сессию


# Обновление автоплатежа
@router.put("/autopayment/{autopayment_id}", response_model=AutoPaymentOut, tags=["autopayments"])
def update_autopayment(autopayment_id: int, autopayment: AutoPaymentUpdate):
    db = get_db_session()  # Создаем сессию вручную
    try:
        result = a_service.update_autopayment(
            db=db,
            autopayment_id=autopayment_id,
            updates=autopayment.dict(exclude_unset=True)
        )
        if not result:
            raise HTTPException(status_code=404, detail="Autopayment not found")

        # Формируем ответ в нужном формате
        return {
            "title": result.title,
            "amount": result.amount,
            "payment_date": result.payment_date
        }
    finally:
        db.close()  # Закрываем сессию


# Получение всех автоплатежей для определенного пользователя
@router.get("/autopayments", response_model=list[AutoPaymentOut], tags=["autopayments"])
def get_all_autopayments(user_id: int):  # Добавлен параметр user_id
    db = get_db_session()  # Создаем сессию вручную
    try:
        result = a_service.get_all_autopayments(db=db, user_id=user_id)  # Передаем user_id в сервис
        if not result:
            raise HTTPException(status_code=404, detail="No autopayments found for user")

        # Формируем ответ в нужном формате
        return [
            {
                "title": item.title,
                "amount": item.amount,
                "payment_date": item.payment_date,
                "merchant_name": item.merchant_name  # Добавляем merchant_name
            }
            for item in result
        ]
    finally:
        db.close()  # Закрываем сессию


# Получение автоплатежа по ID
@router.get("/autopayment/{autopayment_id}", response_model=AutoPaymentOut, tags=["autopayments"])
def get_autopayment_by_id(autopayment_id: int):
    db = get_db_session()  # Создаем сессию вручную
    try:
        result = a_service.get_autopayment_by_id(db=db, autopayment_id=autopayment_id)
        if not result:
            raise HTTPException(status_code=404, detail="Autopayment not found")

        # Формируем ответ в нужном формате
        return {
            "title": result.title,
            "amount": result.amount,
            "payment_date": result.payment_date,
            "merchant_name": result.merchant_name  # Добавляем merchant_name

        }
    finally:
        db.close()  # Закрываем сессию
