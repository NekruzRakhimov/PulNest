
import datetime

from sqlalchemy.orm import Session

from db.postgres import engine
from db.models import Card
from logger.logger import logger

    

def add_card(user_id, card: Card):
    logger.info(f"Adding new card... user_id={user_id}")
    try:
        with Session(bind=engine) as db:
            card_db = Card(user_id=user_id,
                        card_number=card.card_number,
                        card_holder_name=card.card_holder_name,
                        exp_date=card.exp_date,
                        cvv=card.cvv)
            db.add(card_db)
            db.commit()
            logger.info(f"Card added successfully: id={card_db.id}")
            return card_db.id
    except Exception as e:
        return None
    


def get_card_by_id(user_id, card_id):
    logger.info(f"Getting card by ID... user_id={user_id}, card_id={card_id}")
    with Session(bind=engine) as db:
        db_card = db.query(Card).filter(Card.deleted_at == None, Card.user_id == user_id,
                                        Card.id == card_id).first()
        if db_card is None:
            return None
        
        logger.info(f"Card found: id={db_card.id}")
        return db_card
    
    

def get_all_cards(user_id):
    logger.info(f"Getting all cards... user_id={user_id}")
    with Session(bind=engine) as db:
        db_cards = db.query(Card).filter(Card.deleted_at == None, Card.user_id == user_id).all()
        logger.info(f"Found {len(db_cards)} cards for user_id={user_id}")
        return db_cards

def unique_check(card):
    with Session(bind=engine) as db:
        db_card = db.query(Card).filter(Card.card_number == card).first()
        if db_card is None:
            return None
        
        logger.info(f"Card found: id={db_card.id}")
        return db_card
    
def update_card(user_id, card_id, c: Card):
    logger.info(f"Updating card... user_id={user_id}, card_id={card_id}")
    with Session(bind=engine) as db:
        db_card = db.query(Card).filter(Card.deleted_at == None, Card.user_id == user_id,
                                        Card.id == card_id).first()
        if db_card is None:
            logger.warning(f"Card not found for update: user_id={user_id}, card_id={card_id}")
            return None
        db_card.card_number = c.card_number
        db_card.card_holder_name = c.card_holder_name
        db_card.exp_date = c.exp_date
        db_card.cvv = c.cvv
        db.commit()
        db.refresh(db_card)
        logger.info(f"Card updated successfully: id={db_card.id}")
        return db_card.id
      
    
    
def delete_card(user_id, card_id):
    logger.info(f"Deleting card... user_id={user_id}, card_id={card_id}")
    with Session(bind=engine) as db:
        db_card = db.query(Card).filter(Card.deleted_at == None, Card.user_id == user_id,
                                        Card.id == card_id).first()
        if db_card is None:
            return None
        
        db_card.deleted_at = datetime.datetime.now()
        db.commit()
        logger.info(f"Card deleted successfully: id={db_card.id}")
        return db_card.id
    
def expense_card_balance(user_id, card_id, amount):
    with Session(bind=engine) as db:
        db_card = db.query(Card).filter(Card.deleted_at == None, Card.user_id == user_id,
                                        Card.id == card_id).first()
        
        if db_card is None:
            return None
        
        db_card.balance -= amount
        db.commit()
        db.refresh(db_card)
        return db_card
        

def income_card_balance(user_id, amount, card_id,):
    with Session(bind=engine) as db:
        db_card = db.query(Card).filter(Card.deleted_at == None, Card.user_id == user_id,
                                        Card.id == card_id).first()
        
        if db_card is None:
            return None
        
        db_card.balance += amount
        db.commit()
        db.refresh(db_card)
        logger.info(f"Balance updated: card_id={db_card.id}, new_balance={db_card.balance}")
        return db_card


    
def update_card_balance(user_id, card_id, card_balance):
    with Session(bind=engine) as db:
        db_card = db.query(Card).filter(Card.deleted_at == None, Card.user_id == user_id,
                                        Card.id == card_id).first()
        if db_card is None:
            return None
        
        db_card.balance = card_balance()
        db.commit()
        return db_card.id

        
def get_deleted_cards(user_id):
    logger.info(f"Getting deleted cards... user_id={user_id}")
    with Session(bind=engine) as db:
        db_cards = db.query(Card).filter(Card.deleted_at != None, Card.user_id == user_id).all()
        logger.info(f"Found {len(db_cards)} deleted cards for user_id={user_id}")
        return db_cards


    
def get_card_by_card_number(card_number):
    logger.info(f"Searching card by PAN... card_number={card_number}")
    with Session(bind=engine) as db:
        db_card = db.query(Card).filter(Card.deleted_at == None,
                                        Card.card_number == card_number).first()
        if db_card is None:
            logger.warning(f"Card not found by PAN: card_number={card_number}")
            return None
        logger.info(f"Card found: id={db_card.id}, user_id={db_card.user_id}")
        return db_card
    
    




        

        
        

    



