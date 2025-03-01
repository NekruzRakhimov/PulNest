
from sqlalchemy.orm import Session
from db.postgres import engine
from db.models import Card
import datetime

def add_card(user_id, card: Card):
    with Session(bind=engine) as db:
        card_db = Card(user_id=user_id,
                       card_number=card.card_number,
                       card_holder_name=card.card_holder_name,
                       exp_date=card.exp_date,
                       cvv = card.cvv)
        db.add(card_db)
        db.commit()
        return card_db.id
    
def get_card_by_id(user_id, card_id):
    with Session(bind=engine) as db:
        db_card = db.query(Card).filter(Card.deleted_at == None, Card.user_id == user_id,
                                        Card.id == card_id).first()
        
        if db_card is None:
            return None
        
        card = Card()
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
        db_cards = db.query(Card).filter(Card.deleted_at == None,
                                         Card.user_id == user_id).all()

        cards = list()
        for db_card in db_cards:
            card = Card() 
            card.id = db_card.id
            card.user_id = db_card.user_id
            card.card_number = db_card.card_number
            card.card_holder_name = db_card.card_holder_name
            card.exp_date = db_card.exp_date
            card.cvv = db_card.cvv
            card.balance = db_card.balance
            card.created_at = db_card.created_at  
            card.deleted_at = db_card.deleted_at
            
            cards.append(card)
        return cards


def update_card(user_id, card_id, c: Card):
    with Session(bind=engine) as db:
        db_card = db.query(Card).filter(Card.deleted_at == None, Card.user_id == user_id,
                                        Card.id == card_id).first()
        
        if db_card is None:
            return None


        db_card.card_number = c.card_number
        db_card.card_holder_name = c.card_holder_name
        db_card.exp_date = c.exp_date
        db_card.cvv = c.cvv
        db.commit()  
        db.refresh(db_card)  
        return db_card.id  
      
def delete_card(user_id, card_id):
    with Session(bind=engine) as db:
        db_card = db.query(Card).filter(Card.deleted_at == None, Card.user_id == user_id,
                                        Card.id == card_id).first()
        
        if db_card is None:
            return None
        
        db_card.deleted_at = datetime.datetime.now()
        db.commit()
        return db_card.id
        

def get_deleted_cards(user_id):
    with Session(bind=engine) as db:
        db_cards = db.query(Card).filter(Card.deleted_at != None,
                                         Card.user_id == user_id).all()

        cards = list()
        for db_card in db_cards:
            card = Card() 
            card.id = db_card.id
            card.user_id = db_card.user_id
            card.card_number = db_card.card_number
            card.card_holder_name = db_card.card_holder_name
            card.exp_date = db_card.exp_date
            card.cvv = db_card.cvv
            card.balance = db_card.balance
            card.created_at = db_card.created_at  
            card.deleted_at = db_card.deleted_at
            
            cards.append(card)
        return cards




        

        
        

    



