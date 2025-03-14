from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from pkg.controllers.middlewares import get_current_user
from pkg.services import cards as cards_service
from pkg.services import transactions as transactions_service
from pkg.services import wallet as wallet_service
from schemas.cards import CardTransferCard, CardTransferWallet
from schemas.wallet import WalletTransferWallet, WalletTransferCard
from utils.auth import TokenPayload
from schemas.transaction import WalletPaymentSchema, CardPaymentSchema



from logger.logger import logger



router = APIRouter()


TRANSACTION_STATUS_SUCCESS = "success"
TRANSACTION_STATUS_FAILED = "failed"
EXPENSE_TYPE = "expense"
INCOME_TYPE = "income"


def log_card_error(card_number: str, error_message: str):
    logger.error(f"Card {card_number[:4]}****{card_number[-4:]}: {error_message}")

@router.put("/card-card/", summary="Transfer money from card to card", tags=["transactions"])
def expense_card_balance(request: CardTransferCard, payload: TokenPayload = Depends(get_current_user)):
    user_id = payload.id

    sender_card = cards_service.get_card_by_card_number(request.sender_card_number)
    if sender_card is None:
        log_card_error(request.sender_card_number, 'Sender card not found')
        return JSONResponse(
            content={'error': 'Sender card not found'},
            status_code=status.HTTP_404_NOT_FOUND
        )

    receiver_card = cards_service.get_card_by_card_number(request.receiver_card_number)
    if receiver_card is None:
        log_card_error(request.receiver_card_number, 'Receiver card not found')
        return JSONResponse(
            content={'error': 'Receiver card not found'},
            status_code=status.HTTP_404_NOT_FOUND
        )

    # Списание средств
    expense_sender = cards_service.expense_card_balance(user_id, request.amount, sender_card.balance, sender_card.id)
    if expense_sender is None:
        log_card_error(request.sender_card_number, 'Error debiting card')
        return JSONResponse(
            content={'error': 'Something went wrong while debiting the card'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    elif expense_sender == -1:
        log_card_error(request.sender_card_number, 'Insufficient funds')
        return JSONResponse(
            content={'error': 'Insufficient funds'},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # Пополнение средств
    income_receiver = cards_service.income_card_balance(receiver_card.user_id, request.amount, receiver_card.balance, receiver_card.id)
    if income_receiver is None:
        cards_service.income_card_balance(user_id, request.amount, sender_card.balance, sender_card.id)
        transactions_service.card_to_card(user_id, sender_card.id, sender_card.card_number, receiver_card.id, receiver_card.card_number, request.amount, TRANSACTION_STATUS_FAILED, request.comment, EXPENSE_TYPE)
        log_card_error(request.receiver_card_number, 'Error crediting card')
        return JSONResponse(
            content={'error': 'Something went wrong while crediting the card'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    elif income_receiver == -2:
        cards_service.income_card_balance(user_id, request.amount, sender_card.balance, sender_card.id)
        transactions_service.card_to_card(user_id, sender_card.id, sender_card.card_number, receiver_card.id, receiver_card.card_number, request.amount, TRANSACTION_STATUS_FAILED, request.comment, EXPENSE_TYPE)
        log_card_error(request.receiver_card_number, 'Amount exceeds the maximum allowed value')
        return JSONResponse(
            content={'error': 'Amount exceeds the maximum allowed value: 9 999 999 999.99'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    e = transactions_service.card_to_card(user_id, sender_card.id, sender_card.card_number, receiver_card.id, receiver_card.card_number, request.amount, TRANSACTION_STATUS_SUCCESS, request.comment, EXPENSE_TYPE)
    i = transactions_service.card_to_card(receiver_card.user_id, sender_card.id, sender_card.card_number, receiver_card.id, receiver_card.card_number, request.amount, TRANSACTION_STATUS_SUCCESS, request.comment, INCOME_TYPE)
    
    if e and i:
        transactions_service.add_correlation_id(e, i)
        transactions_service.add_correlation_id(i, e)
        return JSONResponse(
            content={'message': 'Transaction successful'},
            status_code=status.HTTP_200_OK
        )
    else:
        log_card_error(f"{request.sender_card_number} to {request.receiver_card_number}", 'Transaction failed')
        return JSONResponse(
            content={'error': 'Something went wrong'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    

@router.put("/wallet-wallet/", summary="Transfer money from wallet to wallet", tags=["transactions"])
def expense_wallet_balance(request: WalletTransferWallet, payload: TokenPayload = Depends(get_current_user)):
    user_id = payload.id

    sender_wallet = wallet_service.get_wallet(user_id)
    if sender_wallet is None:
        logger.info(user_id, 'Sender wallet not found')
        return JSONResponse(
            content={'error': 'Sender wallet not found'},
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    receiver_wallet = wallet_service.get_wallet_by_phone(request.receiver_wallet_number)
    if receiver_wallet is None:
        logger.info(request.receiver_wallet_number, 'Receiver wallet not found')
        return JSONResponse(
            content={'error': 'Receiver wallet not found'},
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    # Списание средств
    expense_sender = wallet_service.wallet_withdrawal(user_id, request.amount)
    if expense_sender is None:
        logger.info(sender_wallet.phone, 'Error debiting wallet')
        return JSONResponse(
            content={'error': 'Something went wrong while debiting the wallet'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    elif expense_sender == -1:
        logger.info(sender_wallet.phone, 'Insufficient funds')
        return JSONResponse(
            content={'error': 'Insufficient funds'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    # Пополнение средств
    income_receiver = wallet_service.wallet_topup(receiver_wallet.user_id, request.amount)
    if income_receiver is None:
        wallet_service.wallet_topup(user_id, request.amount)
        e = transactions_service.wallet_to_wallet(user_id, sender_wallet.id, sender_wallet.phone, receiver_wallet.id, receiver_wallet.phone
                                              , request.amount, TRANSACTION_STATUS_FAILED, request.comment, EXPENSE_TYPE)
        logger.info(receiver_wallet.user_id, 'Error crediting wallet')
        return JSONResponse(
            content={'error': 'Something went wrong while crediting the wallet'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    
    e = transactions_service.wallet_to_wallet(user_id, sender_wallet.id, sender_wallet.phone, receiver_wallet.id, receiver_wallet.phone
                                              , request.amount, TRANSACTION_STATUS_SUCCESS, request.comment, EXPENSE_TYPE)
    i = transactions_service.wallet_to_wallet(receiver_wallet.user_id, sender_wallet.id, sender_wallet.phone, receiver_wallet.id, receiver_wallet.phone
                                              , request.amount, TRANSACTION_STATUS_SUCCESS, request.comment, INCOME_TYPE)
    
    if e and i:
        transactions_service.add_correlation_id(e, i)
        transactions_service.add_correlation_id(i, e)
        return JSONResponse(
            content={'message': 'Transaction successful'},
            status_code=status.HTTP_200_OK
        )
    else:
        logger.info(f"{sender_wallet.phone} to {receiver_wallet.phone}", 'Transaction failed')
        return JSONResponse(
            content={'error': 'Something went wrong'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    

@router.put("/card-wallet/", summary="Transfer money from card to wallet", tags=["transactions"])
def expense_card_income_wallet(request: CardTransferWallet, payload: TokenPayload = Depends(get_current_user)):
    user_id = payload.id

    sender_card = cards_service.get_card_by_card_number(request.sender_card_number)
    if sender_card is None:
        logger.info(f'{request.sender_card_number[:4]}****{request.sender_card_number[-4:]}', 'Sender card not found')
        return JSONResponse(
            content={'error': 'Sender card not found'},
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    receiver_wallet = wallet_service.get_wallet_by_phone(request.receiver_wallet_number)
    if receiver_wallet is None:
        logger.info(request.receiver_wallet_number, 'Receiver wallet not found')
        return JSONResponse(
            content={'error': 'Receiver wallet not found'},
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    # Списание средств
    expense_sender = cards_service.expense_card_balance(user_id, request.amount, sender_card.balance, sender_card.id)
    if expense_sender is None:
        logger.info(f'{request.sender_card_number[:4]}****{request.sender_card_number[-4:]}', 'Error debiting card')
        return JSONResponse(
            content={'error': 'Something went wrong while debiting the card'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    elif expense_sender == -1:
        logger.info(f'{request.sender_card_number[:4]}****{request.sender_card_number[-4:]}', 'Insufficient funds')
        return JSONResponse(
            content={'error': 'Insufficient funds'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    

     # Пополнение средств
    income_receiver = wallet_service.wallet_topup(receiver_wallet.user_id, request.amount)
    if income_receiver is None:
        cards_service.income_card_balance(user_id, request.amount, sender_card.balance, sender_card.id)
        e = transactions_service.card_to_wallet(user_id, sender_card.id, sender_card.card_number, receiver_wallet.id, receiver_wallet.phone, request.amount, TRANSACTION_STATUS_FAILED, request.comment, EXPENSE_TYPE)
        logger.info(receiver_wallet.user_id, 'Error crediting card')
        return JSONResponse(
            content={'error': 'Something went wrong while crediting the card'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    

    e = transactions_service.card_to_wallet(user_id, sender_card.id, sender_card.card_number, receiver_wallet.id, receiver_wallet.phone, request.amount, TRANSACTION_STATUS_SUCCESS, request.comment, EXPENSE_TYPE)
    i = transactions_service.card_to_wallet(receiver_wallet.user_id, sender_card.id, sender_card.card_number, receiver_wallet.id, receiver_wallet.phone
                                              , request.amount, TRANSACTION_STATUS_SUCCESS, request.comment, INCOME_TYPE)
    
    if e and i:
        transactions_service.add_correlation_id(e, i)
        transactions_service.add_correlation_id(i, e)
        return JSONResponse(
            content={'message': 'Transaction successful'},
            status_code=status.HTTP_200_OK
        )
    else:
        logger.info(f"{request.sender_card_number} to {receiver_wallet.phone}", 'Transaction failed')
        return JSONResponse(
            content={'error': 'Something went wrong'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    

@router.put("/wallet-card/", summary="Transfer money from wallet to card", tags=["transactions"])
def expense_wallet_income_card(request: WalletTransferCard, payload: TokenPayload = Depends(get_current_user)):
    user_id = payload.id

    sender_wallet = wallet_service.get_wallet(user_id)
    if sender_wallet is None:
        logger.info(user_id, 'Sender wallet not found')
        return JSONResponse(
            content={'error': 'Sender wallet not found'},
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    receiver_card = cards_service.get_card_by_card_number(request.receiver_card_number)
    if receiver_card is None:
        logger.info(f'{request.receiver_card_number[:4]}****{request.receiver_card_number[-4:]}', 'Receiver card not found')
        return JSONResponse(
            content={'error': 'Receiver card not found'},
            status_code=status.HTTP_404_NOT_FOUND
        )
    

    # Списание средств
    expense_sender = wallet_service.wallet_withdrawal(user_id, request.amount)
    if expense_sender is None:
        logger.info(sender_wallet.phone, 'Error debiting wallet')
        return JSONResponse(
            content={'error': 'Something went wrong while debiting the wallet'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    elif expense_sender == -1:
        logger.info(sender_wallet.phone, 'Insufficient funds')
        return JSONResponse(
            content={'error': 'Insufficient funds'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    

    # Пополнение средств
    income_receiver = cards_service.income_card_balance(receiver_card.user_id, request.amount, receiver_card.balance, receiver_card.id)
    if income_receiver is None:
        wallet_service.wallet_topup(user_id, request.amount)
        e = transactions_service.wallet_to_card(user_id, sender_wallet.id, sender_wallet.phone, receiver_card.id, receiver_card.card_number, request.amount, TRANSACTION_STATUS_FAILED, request.comment, EXPENSE_TYPE)
        log_card_error(request.receiver_card_number, 'Error crediting card')
        return JSONResponse(
            content={'error': 'Something went wrong while crediting the card'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    elif income_receiver == -2:
        wallet_service.wallet_topup(user_id, request.amount)
        e = transactions_service.wallet_to_card(user_id, sender_wallet.id, sender_wallet.phone, receiver_card.id, receiver_card.card_number, request.amount, TRANSACTION_STATUS_FAILED, request.comment, EXPENSE_TYPE)
        log_card_error(request.receiver_card_number, 'Amount exceeds the maximum allowed value')
        return JSONResponse(
            content={'error': 'Amount exceeds the maximum allowed value: 9 999 999 999.99'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
                                            
    e = transactions_service.wallet_to_card(user_id, sender_wallet.id, sender_wallet.phone, receiver_card.id, receiver_card.card_number, request.amount, TRANSACTION_STATUS_SUCCESS, request.comment, EXPENSE_TYPE)
    i = transactions_service.wallet_to_card(receiver_card.user_id, sender_wallet.id, sender_wallet.phone, receiver_card.id, receiver_card.card_number
                                              , request.amount, TRANSACTION_STATUS_SUCCESS, request.comment, INCOME_TYPE)
    
    if e and i:
        transactions_service.add_correlation_id(e, i)
        transactions_service.add_correlation_id(i, e)
        return JSONResponse(
            content={'message': 'Transaction successful'},
            status_code=status.HTTP_200_OK
        )
    else:
        logger.info(f"{sender_wallet.phone} to {receiver_card.card_number}", 'Transaction failed')
        return JSONResponse(
            content={'error': 'Something went wrong'},
            status_code=status.HTTP_400_BAD_REQUEST
        )


@router.post("/payments/wallet", summary="Make payment via wallet balance", tags=["transactions"])
def wallet_payment(payment_data: WalletPaymentSchema, payload: TokenPayload = Depends(get_current_user)):
    user_id = payload.id
    try:
        result = transactions_service.pay_service_by_wallet(
            user_id=user_id,
            service_id=payment_data.service_id,
            amount=payment_data.amount,
            account_number=payment_data.account_number,
            comment=payment_data.comment
        )

        if result > 0:
            return JSONResponse(content={"message" : "Payment made successfully."}, 
                                status_code=status.HTTP_200_OK)
        
        elif result == -1:
            return JSONResponse(content={"message" : "Transaction declined due to insufficient funds."}, 
                                status_code=status.HTTP_402_PAYMENT_REQUIRED)
        
        elif result == -2:
            return JSONResponse(content={"message" : "Service does not exist."}, 
                                status_code=status.HTTP_400_BAD_REQUEST)
        
        else:
            return JSONResponse(content={"message" : "An error occurred while processing the wallet payment."}, 
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        raise JSONResponse(content={"message" : "An error occurred while processing the wallet payment."}, 
                           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@router.post("/payments/card", summary="Make payment via card balance", tags=["transactions"])
def wallet_payment(payment_data: CardPaymentSchema, payload: TokenPayload = Depends(get_current_user)):
    user_id = payload.id
    try:
        card = cards_service.get_card_by_card_number(payment_data.card_number)
        if card is not None:
            result = transactions_service.pay_service_by_card(
                user_id=user_id,
                service_id=payment_data.service_id,
                card_number=payment_data.card_number,
                amount=payment_data.amount,
                account_number=payment_data.account_number,
                comment=payment_data.comment
            )

            if result > 0:
                return JSONResponse(content={"message" : "Payment made successfully."}, 
                                    status_code=status.HTTP_200_OK)
            
            elif result == -1:
                return JSONResponse(content={"message" : "Transaction declined due to insufficient funds."}, 
                                    status_code=status.HTTP_402_PAYMENT_REQUIRED)
            
            elif result == -2:
                return JSONResponse(content={"message" : "Service does not exist."}, 
                                    status_code=status.HTTP_400_BAD_REQUEST)
            
            else:
                return JSONResponse(content={"message" : "An error occurred while processing the card payment."}, 
                                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        else:
            logger.error(f"Card {payment_data.card_number[:4]}****{payment_data.card_number[-4:]} not found")
            return JSONResponse(
                    content={'error': 'Card not found'},
                    status_code=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        raise JSONResponse(content={"message" : "An error occurred while processing the card payment."}, 
                           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
