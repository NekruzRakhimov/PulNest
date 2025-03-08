import json
from fastapi import APIRouter, status, Depends, HTTPException, Header
from starlette.responses import Response, JSONResponse

from logger.logger import logger
from pkg.controllers.middlewares import get_current_user
from schemas.wallet import WalletBase, WalletBalanceResponse
from pkg.services import wallet as wallet_service
from utils.auth import TokenPayload

router = APIRouter()



@router.get("/wallet-balance")
def get_wallet_balance(payload: TokenPayload = Depends(get_current_user)):
    
    user_id = payload.id
    logger.info(f"Get users wallet balance. Request user: {user_id}")
    balance = wallet_service.get_wallet_balance(user_id)
    return JSONResponse({"Balance": float(balance)}, status_code=status.HTTP_200_OK)

