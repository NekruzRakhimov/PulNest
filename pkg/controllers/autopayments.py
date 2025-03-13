from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.autopayments import AutoPaymentCreate, AutoPaymentOut, AutoPaymentUpdate
from db.postgres import engine
from pkg.services.autopayments import AutoPaymentService
from pkg.repositories.autopayments import AutoPaymentRepository

router = APIRouter()
repository = AutoPaymentRepository()
service = AutoPaymentService(repository)


def get_db_session():
    return Session(bind=engine)


@router.post("/autopayment", response_model=AutoPaymentOut, tags=["autopayments"])
def create_autopayment(autopayment: AutoPaymentCreate, db: Session = Depends(get_db_session)):
    result = service.create_autopayment(db, autopayment.dict())
    if not result:
        raise HTTPException(status_code=400, detail="Failed to create autopayment")
    return result


@router.put("/autopayment/{autopayment_id}", response_model=AutoPaymentOut, tags=["autopayments"])
def update_autopayment(autopayment_id: int, autopayment: AutoPaymentUpdate, db: Session = Depends(get_db_session)):
    result = service.update_autopayment(db, autopayment_id, autopayment.dict(exclude_unset=True))
    if not result:
        raise HTTPException(status_code=404, detail="Autopayment not found")
    return result


@router.get("/autopayments", response_model=list[AutoPaymentOut], tags=["autopayments"])
def get_all_autopayments(user_id: int, db: Session = Depends(get_db_session)):
    result = service.get_all_autopayments(db, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="No autopayments found for user")
    return result


@router.get("/autopayment/{autopayment_id}", response_model=AutoPaymentOut, tags=["autopayments"])
def get_autopayment_by_id(autopayment_id: int, db: Session = Depends(get_db_session)):
    result = service.get_autopayment_by_id(db, autopayment_id)
    if not result:
        raise HTTPException(status_code=404, detail="Autopayment not found")
    return result
