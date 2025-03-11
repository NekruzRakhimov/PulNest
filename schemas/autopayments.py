from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AutoPaymentCreate(BaseModel):
    user_id: int
    amount: float
    service_id: int
    payment_date: Optional[datetime] = None  # Дата платежа может быть опциональной
    is_active: Optional[bool] = True  # Статус активности автоплатежа, по умолчанию True

    class Config:
        orm_mode = True


class AutoPaymentOut(BaseModel):
    id: int
    user_id: int
    amount: float
    service_id: int
    payment_date: datetime
    is_active: bool
    created_at: datetime
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True


class AutoPaymentUpdate(BaseModel):
    amount: Optional[float]
    service_id: Optional[int]
    is_active: Optional[bool]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True



