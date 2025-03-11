from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal


class AutoPaymentCreate(BaseModel):
    user_id: int
    amount: Decimal  # Изменили на Decimal
    service_id: int
    title: str  # Новый атрибут для названия автоплатежа
    payment_date: Optional[datetime] = None  # Дата платежа может быть опциональной
    is_active: Optional[bool] = True  # Статус активности автоплатежа, по умолчанию True

    class Config:
        from_attributes = True  # Используем для Pydantic v2


class AutoPaymentOut(BaseModel):
    title: str  # Название автоплатежа
    merchant_name: Optional[str] = None  # Добавляем merchant_name, он может быть пустым
    amount: Decimal  # Сумма
    payment_date: datetime  # Дата платежа

    class Config:
        from_attributes = True  # Используем для Pydantic v2


class AutoPaymentUpdate(BaseModel):
    amount: Optional[Decimal]  # Сумма
    service_id: Optional[int]  # Сервис
    is_active: Optional[bool]  # Статус активности
    deleted_at: Optional[datetime]  = None  # Дата удаления

    class Config:
        from_attributes = True  # Используем для Pydantic v2
