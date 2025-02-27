from sqlalchemy.orm import Session
from db.models import Cards
from schemas.cards import CardCreate, CardUpdate
from sqlalchemy.exc import SQLAlchemyError

class CardsRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_card(self, user_id: int, card_number: str, card_holder_name: str, exp_date: str, cvv: str):
        try:
            new_card = Cards(
                user_id=user_id,
                card_number=card_number,
                card_holder_name=card_holder_name,
                exp_date=exp_date,
                cvv=cvv,
                created_at=datetime.now(),
                deleted_at=None
            )
            self.db.add(new_card)
            self.db.commit()
            self.db.refresh(new_card)
            return new_card
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def get_card(self, card_id: int):
        return self.db.query(Cards).filter(Cards.id == card_id).first()

    def update_card(self, card_id: int, card_number: str, card_holder_name: str, exp_date: str, cvv: str):
        card = self.db.query(Cards).filter(Cards.id == card_id).first()
        if card:
            card.card_number = card_number
            card.card_holder_name = card_holder_name
            card.exp_date = exp_date
            card.cvv = cvv
            self.db.commit()
            self.db.refresh(card)
        return card

    def delete_card(self, card_id: int):
        card = self.db.query(Cards).filter(Cards.id == card_id).first()
        if card:
            self.db.delete(card)
            self.db.commit()

from sqlalchemy.orm import Session
from db.postgres import engine
from db.models import Cards
import datetime

def add_card(user_id, card: Cards):
    with Session(bind=engine) as db:
        card_db = Cards(user_id=card.user_id,
                       card_number=card.card_number,
                       card_holder_name=card.card_holder_name,
                       exp_date=card.exp_date,
                       cvv = card.cvv)
        db.add(card_db)
        db.commit()
        return card_db.id
    
def get_card_by_id(user_id, card_id):
    with Session(bind=engine) as db:
        db_card = db.query(Cards).filter(Cards.deleted_at == None, Cards.user_id == user_id,
                                        Cards.id == card_id).first()
        
        if db_card is None:
            return None
        
        card = Cards()
        card.id = db_card.id
        card.user_id = db_card.user_id
        card.card_number = db_card.card_number
        card.card_holder_name = db_card.card_holder_name
        card.exp_date = db_card.exp_date
        card.cvv = db_card.cvv
        card.balance = db_card.balance
        card.created_at = db_card.card_number
        card.deleted_at = db_card.deleted_at
        return card


def get_all_cards(user_id):
    with Session(bind=engine) as db:
        db_card = db.query(Cards).filter(Cards.deleted_at == None,
                                         Cards.user_id == user_id).all()

        cards = list()
        for card in db_card:
            card = Cards()
            card.id = db_card.id
            card.user_id = db_card.user_id
            card.card_number = db_card.card_number
            card.card_holder_name = db_card.card_holder_name
            card.exp_date = db_card.exp_date
            card.cvv = db_card.cvv
            card.balance = db_card.balance
            card.created_at = db_card.card_number
            card.deleted_at = db_card.deleted_at
           
            cards.append(card)
        return cards


