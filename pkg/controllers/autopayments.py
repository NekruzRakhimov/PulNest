from fastapi import APIRouter, HTTPException
from schemas.autopayments import AutoPaymentCreate, AutoPaymentOut, AutoPaymentUpdate
from pkg.services import autopayments as a_service

router = APIRouter()


# Создание автоплатежа
@router.post("/autopayment", response_model=AutoPaymentOut, tags=["autopayments"])
def create_autopayment(autopayment: AutoPaymentCreate):
    result = a_service.create_autopayment(
        user_id=autopayment.user_id,
        amount=autopayment.amount,
        service_id=autopayment.service_id
    )
    if not result:
        raise HTTPException(status_code=400, detail="Failed to create autopayment")
    return result


# Обновление автоплатежа
@router.put("/autopayment/{autopayment_id}", response_model=AutoPaymentOut, tags=["autopayments"])
def update_autopayment(autopayment_id: int, autopayment: AutoPaymentUpdate):
    result = a_service.update_autopayment(autopayment_id, autopayment.dict(exclude_unset=True))
    if not result:
        raise HTTPException(status_code=404, detail="Autopayment not found")
    return result
