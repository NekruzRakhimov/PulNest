import json
from fastapi import APIRouter, status, Depends, HTTPException, Header
from starlette.responses import Response, JSONResponse

from logger.logger import logger
from pkg.controllers.middlewares import get_current_user
from schemas.wallet import WalletBase
from pkg.services import wallet as wallet_service
from utils.auth import TokenPayload

router = APIRouter()


@router.get("/wallet", summary="Get user's wallet info",  tags=["walltes"])
def get_wallet(payload: TokenPayload = Depends(get_current_user)):
    user_id = payload.id
    logger.info(f"Get wallet for user {user_id}.")

    try:
        wallet = wallet_service.get_wallet(user_id)
        if wallet:
            wallet_response = WalletBase(
                phone=wallet.phone,
                balance=wallet.balance,
                bonus_balance=wallet.bonus_balance
            )

            return JSONResponse({"Walet Info": wallet_response.dict()}, status_code=status.HTTP_200_OK)

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wallet not found"
            )
    except Exception as e:
        logger.error(f"Error retrieving wallet for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the wallet"
        )


@router.get("/wallet-balance", summary="Get user's wallet balance",  tags=["walltes"])
def get_wallet_balance(payload: TokenPayload = Depends(get_current_user)):
    user_id = payload.id
    logger.info(f"Get wallet balance for user {user_id}.")

    try:
        balance = wallet_service.get_wallet_balance(user_id)
        if balance is not None:
            return JSONResponse({"Balance": float(balance)}, status_code=status.HTTP_200_OK)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wallet not found"
            )
    except Exception as e:
        logger.error(f"Error retrieving wallet balance for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the balance"
        )