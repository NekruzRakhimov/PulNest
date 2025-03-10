from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from pkg.controllers.middlewares import get_current_user
from pkg.services import cards as cards_service
from pkg.services import transactions as transactions_service
from schemas.cards import CardTransferCard
from utils.auth import TokenPayload

router = APIRouter()

from logger.logger import logger

@router.put("/card-card/", summary="Transfer money from card to card", tags=["transactions"])
def expense_card_balance(request: CardTransferCard, payload: TokenPayload = Depends(get_current_user)):
    user_id = payload.id

    sender_card = cards_service.get_card_by_card_number(user_id, request.sender_card_number)
    if sender_card is None:
        logger.error(f"Sender card {request.sender_card_number[:4]}****{request.sender_card_number[-4:]} not found")
        return JSONResponse(
            content={'error': 'Sender card not found'},
            status_code=status.HTTP_404_NOT_FOUND
        )

    receiver_card = cards_service.get_card_by_card_number(user_id, request.receiver_card_number)
    if receiver_card is None:
        logger.error(f"Receiver card {request.receiver_card_number[:4]}****{request.receiver_card_number[-4:]} not found")
        return JSONResponse(
            content={'error': 'Receiver card not found'},
            status_code=status.HTTP_404_NOT_FOUND
        )

    # Списание средств
    expense_sender = cards_service.expense_card_balance(user_id, request.amount, sender_card.balance, sender_card.id)
    if expense_sender is None:
        logger.error(f"Error debiting card {request.sender_card_number[:4]}****{request.sender_card_number[-4:]} for amount {request.amount}")
        return JSONResponse(
            content={'error': 'Something went wrong while debiting the card'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    elif expense_sender == -1:
        logger.error(f"Insufficient funds on card {request.sender_card_number[:4]}****{request.sender_card_number[-4:]}")
        return JSONResponse(
            content={'error': 'Insufficient funds'},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # Если списание неудачное, фиксируем неудачную транзакцию
    if expense_sender in [None, -1]:
        logger.error(f"Failed transaction between {request.sender_card_number[:4]}****{request.sender_card_number[-4:]} and {request.receiver_card_number[:4]}****{request.receiver_card_number[-4:]}")
        transaction_status = "failed"
        transactions_service.card_to_card(user_id, sender_card.id, receiver_card.id, request.amount, transaction_status)
        return JSONResponse(
            content={'error': 'Transaction failed'},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # Пополнение средств
    income_receiver = cards_service.income_card_balance(user_id, request.amount, receiver_card.balance, receiver_card.id)
    if income_receiver is None:
        logger.error(f"Error crediting card {request.receiver_card_number[:4]}****{request.receiver_card_number[-4:]} for amount {request.amount}")
        return JSONResponse(
            content={'error': 'Something went wrong while crediting the card'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    elif income_receiver == -2:
        logger.error(f"Amount exceeds the maximum allowed value for card {request.receiver_card_number[:4]}****{request.receiver_card_number[-4:]}")
        return JSONResponse(
            content={'error': 'Amount exceeds the maximum allowed value: 9 999 999 999.99'},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # Фиксация успешной транзакции
    transaction_status = "success"
    transactions_service.card_to_card(user_id, sender_card.id, sender_card.card_number, receiver_card.id, receiver_card.card_number, request.amount, transaction_status) 

    return JSONResponse(
        content={'message': 'Transaction successful'},
        status_code=status.HTTP_200_OK
    )
