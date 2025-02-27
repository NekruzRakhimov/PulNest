import json

from fastapi import APIRouter, status, Depends

from starlette.responses import Response

# from pkg.controllers.user import get_current_user, TokenPayload
from pkg.services import cards as cards_service
from schemas.cards import CardResponse

router = APIRouter()



@router.post("/cards", summary="Create new card", tags=["cards"])
def add_card(card: CardResponse):
    user_id = 1
    new_card = cards_service.add_card(user_id, card)
    if new_card is None:
        return Response(json.dumps({'error': 'something went wrong while creating the card'}), status.HTTP_400_BAD_REQUEST)
    
    return Response(json.dumps({'message': 'successfully added new card'}), status_code=201,
                    media_type='application/json')

@router.get("/cards/{card_id}", summary="Get card by ID", tags=["cards"])
def get_card_by_id(card_id: int):
    user_id = 1
    card = cards_service.get_card_by_id(user_id, card_id)
    if card is None:
        return Response(json.dumps({'error': 'card not found'}), status.HTTP_404_NOT_FOUND)
    return card

@router.get("/cards", summary="Get all cards", tags=["cards"])
def get_all_cards(response: Response):
    user_id = 1
    cards = cards_service.get_all_cards(user_id)
    response.status_code = status.HTTP_200_OK
    response.headers["Content-Type"] = "application/json"
    return cards

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
