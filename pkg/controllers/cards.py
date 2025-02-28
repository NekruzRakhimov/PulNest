import json

from fastapi import APIRouter, status

from fastapi.responses import JSONResponse

# from pkg.controllers.user import get_current_user, TokenPayload
from pkg.services import cards as cards_service
from schemas.cards import CardCreate

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



@router.get("/cards/{card_id}", summary="Get card by ID", tags=["cards"])
def get_card_by_id(card_id: int):
    user_id = 1 
    card = cards_service.get_card_by_id(user_id, card_id)
    
    if card is None:
        return JSONResponse(
            content={'error': 'Card not found'},
            status_code=status.HTTP_404_NOT_FOUND
        )
    

    return JSONResponse(
        content={'card': card},
        status_code=status.HTTP_200_OK
    )

@router.get("/cards", summary="Get all cards", tags=["cards"])
def get_all_cards():
    user_id = 1  
    cards = cards_service.get_all_cards(user_id)
    
    return JSONResponse(
        content={'cards': cards},
        status_code=status.HTTP_200_OK
    )


# @router.put("/cards/{card_id}", response_model=CardResponse)
# def update_card(card_id: int, card: CardUpdate, service: CardsService = Depends()):
#     try:
#         return service.update_card(card_id, card)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @router.delete("/cards/{card_id}")
# def delete_card(card_id: int, service: CardsService = Depends()):
#     try:
#         service.delete_card(card_id)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
