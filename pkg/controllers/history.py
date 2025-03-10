from fastapi import APIRouter, Depends, status, Query
from fastapi.responses import JSONResponse

from utils.auth import TokenPayload
from pkg.controllers.middlewares import get_current_user
from pkg.services import history as history_service
from datetime import date
from decimal import Decimal



router = APIRouter()

@router.get("/history/all/", summary="Get all transactions for the user", tags=["transactions"])
def get_all_transactions(payload: TokenPayload = Depends(get_current_user)):
    user_id = payload.id
    history = history_service.get_all_transactions(user_id)

    history_dict = [h.model_dump() for h in history]
    return JSONResponse(
        content={'history': history_dict},
        status_code=status.HTTP_200_OK
    )



@router.get("/history/amount/", summary="Get transactions by amount range", tags=["transactions"])
def get_transactions_by_amount(
    min_amount: Decimal = Query(..., description="Minimum transaction amount"),  
    max_amount: Decimal = Query(..., description="Maximum transaction amount"), 
    payload: TokenPayload = Depends(get_current_user)
):
    user_id = payload.id
    history = history_service.get_transactions_by_amount(user_id, min_amount, max_amount)

    history_dict = [h.model_dump() for h in history]
    return JSONResponse(
        content={'history': history_dict},
        status_code=status.HTTP_200_OK
    )



@router.get("/history/date/", summary="Get transactions by date range", tags=["transactions"])
def get_transactions_by_date(
    start_date: date = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: date = Query(..., description="End date in YYYY-MM-DD format"),
    payload: TokenPayload = Depends(get_current_user)
):
    user_id = payload.id
    history = history_service.get_transactions_by_date(user_id, start_date, end_date)

    history_dict = [h.model_dump() for h in history]
    return JSONResponse(
        content={'history': history_dict},
        status_code=status.HTTP_200_OK
    )


