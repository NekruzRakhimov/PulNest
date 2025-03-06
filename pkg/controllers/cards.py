from fastapi import APIRouter, status

from fastapi.responses import JSONResponse

from logger.logger import logger
# from pkg.controllers.user import get_current_user, TokenPayload
from pkg.services import cards as cards_service
from schemas.cards import CardCreate, CardUpdate



router = APIRouter()



@router.post("/cards", summary="Create new card", tags=["cards"])
def add_card(card: CardCreate):
    user_id = 1  
    new_card = cards_service.add_card(user_id, card)
    
    if new_card is None:
        return JSONResponse(
            content={'error': 'Something went wrong while creating the card'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    return JSONResponse(
        content={'message': 'Successfully added new card'},
        status_code=status.HTTP_201_CREATED
    )



@router.get("/cards", summary="Get all cards", tags=["cards"])
def get_all_cards():
    user_id = 1  
    cards = cards_service.get_all_cards(user_id)
    
    cards_dict = [card.model_dump() for card in cards]

    
    return JSONResponse(
        content={'cards': cards_dict},
        status_code=status.HTTP_200_OK
    )



@router.put("/cards/{card_id}/update", summary="Update card by ID", tags=["cards"])
def update_card(card_id: int, card: CardUpdate):
    user_id = 1

    got_by_id = cards_service.get_card_by_id(user_id, card_id)
    if got_by_id is None:
         return JSONResponse(
            content={'error': 'Card not found'},
            status_code=status.HTTP_404_NOT_FOUND
    )

    updated_card = cards_service.update_card(user_id, card_id, card)
    if updated_card is None:
        return JSONResponse(
            content={'error': 'Something went wrong while updating the card'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    return JSONResponse(
        content={'message': 'Successfully updated new card'},
        status_code=status.HTTP_200_OK
    )



@router.delete("/cards/{card_id}/delete", summary="Delete task by ID", tags=["cards"])
def delete_task(card_id: int):
    user_id = 1

    card = cards_service.get_card_by_id(user_id, card_id)
    if card is None:
        return JSONResponse(
            content={'error': 'Card not found'},
            status_code=status.HTTP_404_NOT_FOUND
        )



    deleted_task =cards_service.delete_card(user_id, card_id)
    if deleted_task is None:
        return JSONResponse(
            content={'error': 'Something went wrong while deleting the card'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    return JSONResponse(
        content={'message': 'Successfully deleted card'},
        status_code=status.HTTP_200_OK
    )



@router.get("/deleted-cards", summary="Get all deleted cards", tags=["cards"])
def get_deleted_cards():
    user_id = 1  
    cards = cards_service.get_deleted_cards(user_id)
    
    cards_dict = [card.model_dump() for card in cards]

    
    return JSONResponse(
        content={'cards': cards_dict},
        status_code=status.HTTP_200_OK
    )



@router.get("/cards/{card_number}/number", summary="Get card by PAN", tags=["cards"])
def get_card_by_number(card_number: str):
    logger.info(card_number)
    user_id = 1 
    card = cards_service.get_card_by_card_number(user_id, card_number)
    if card is None:
        return JSONResponse(
            content={'error': 'Card not found'},
            status_code=status.HTTP_404_NOT_FOUND
        )

    return JSONResponse(
        content={'card': card.model_dump()},
        status_code=status.HTTP_200_OK
    )



@router.get("/cards/{card_id}/details", summary="Get card by ID", tags=["cards"])
def get_card_by_id(card_id: int):
    user_id = 1 
    card = cards_service.get_card_by_id(user_id, card_id)

    if card is None:
        return JSONResponse(
            content={'error': 'Card not found'},
            status_code=status.HTTP_404_NOT_FOUND
    )

    return JSONResponse(
        content={'card': card.model_dump()},
        status_code=status.HTTP_200_OK
    )





    
    

    

 
        


