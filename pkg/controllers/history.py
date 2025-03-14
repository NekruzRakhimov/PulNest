from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends, status, Query
from fastapi.responses import JSONResponse

from utils.auth import TokenPayload
from pkg.controllers.middlewares import get_current_user
from pkg.services import history as history_service


router = APIRouter()

@router.get("/history/", summary="Get transactions with optional filters", tags=["history"])
def get_transactions(
    min_amount: Decimal | None = Query(None, description="Minimum transaction amount"),  
    max_amount: Decimal | None = Query(None, description="Maximum transaction amount"), 
    start_date: date | None = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: date | None = Query(None, description="End date in YYYY-MM-DD format"),
    state: str | None = Query(None, description="Status of transaction"),
    tran_type: str | None = Query(None, description="Type of transaction"),
    source_type: str | None = Query(None, description="Source type of transaction"),
    dest_type: str | None = Query(None, description="Source type of transaction"),
    payload: TokenPayload = Depends(get_current_user)
):
    user_id = payload.id
    history = history_service.get_transactions(user_id, min_amount, max_amount, start_date, end_date, state, tran_type, source_type, dest_type)

    history_dict = [h.model_dump() for h in history]
    return JSONResponse(
        content={'history': history_dict},
        status_code=status.HTTP_200_OK
    )

