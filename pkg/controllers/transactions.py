from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from pkg.services import cards as cards_service
from pkg.services import transactions as transactions_service
from schemas.cards import CardTransferCard

router = APIRouter()


@router.put("/card-card/", summary="Transfer money from card to card", tags=["transactions"])
def expense_card_balance(request: CardTransferCard):
    user_id = 1  # TODO: Получать реального пользователя

    sender_card = cards_service.get_card_by_card_number(user_id, request.sender_card_number)
    if sender_card is None:
        return JSONResponse(
            content={'error': 'Sender card not found'},
            status_code=status.HTTP_404_NOT_FOUND
        )

    receiver_card = cards_service.get_card_by_card_number(user_id, request.receiver_card_number)
    if receiver_card is None:
        return JSONResponse(
            content={'error': 'Receiver card not found'},
            status_code=status.HTTP_404_NOT_FOUND
        )

    # Списание средств
    expense_sender = cards_service.expense_card_balance(user_id, request.amount, sender_card)
    if expense_sender is None:
        return JSONResponse(
            content={'error': 'Something went wrong while debiting the card'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    elif expense_sender == -1:
        return JSONResponse(
            content={'error': 'Insufficient funds'},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # Если списание неудачное, фиксируем неудачную транзакцию
    if expense_sender is not True:
        transaction_status = "failed"
        transactions_service.card_to_card(user_id, sender_card.id, receiver_card.id, request.amount, transaction_status)
        return JSONResponse(
            content={'error': 'Transaction failed'},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # Пополнение средств
    income_receiver = cards_service.income_card_balance(user_id, request.amount, receiver_card)
    if income_receiver is None:
        return JSONResponse(
            content={'error': 'Something went wrong while crediting the card'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    elif income_receiver == -2:
        return JSONResponse(
            content={'error': 'Amount exceeds the maximum allowed value: 9 999 999 999.99'},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # Фиксация успешной транзакции
    transaction_status = "success"
    transactions_service.card_to_card(user_id, sender_card.id, receiver_card.id, request.amount, transaction_status)

    return JSONResponse(
        content={'message': 'Transaction successful'},
        status_code=status.HTTP_200_OK
    )
