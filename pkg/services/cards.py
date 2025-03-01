from db.models import Card
from pkg.repositories import cards as cards_repository
from schemas.cards import CardCreate, CardReturn, CardUpdate
from cryptography.fernet import Fernet
from logger.logger import logger



cipher_suite = Fernet(b'J7IkzyQSkS9zWj9b_s0NOc8X1xKHcN5Mm3DRzRaP4hQ=')

def encrypt_data(data: str) -> str:
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt_data(data: str) -> str:
    return cipher_suite.decrypt(data.encode()).decode()

def add_card(user_id, card: CardCreate):
    encrypted_card_number = encrypt_data(card.card_number)
    encrypted_cvv = encrypt_data(card.cvv)
    
    c = Card(
        user_id=user_id,
        card_number=encrypted_card_number,
        card_holder_name=card.card_holder_name,
        exp_date=card.exp_date,
        cvv=encrypted_cvv
    )
    
    
    logger.info(f"Adding card: user_id={user_id}, card_number={encrypted_card_number}, cvv={encrypted_cvv}")
    return cards_repository.add_card(user_id, c)




def get_card_by_id(user_id, card_id):
    card = cards_repository.get_card_by_id(user_id, card_id)
    decrypted_card_number = decrypt_data(card.card_number)
    
    c = CardReturn(
        card_holder_name=card.card_holder_name,
        card_number=decrypted_card_number,
        exp_date=card.exp_date,
        balance=card.balance
    )
    
    return c
    
   

def get_all_cards(user_id):
    cards = cards_repository.get_all_cards(user_id)
    card_list = []
    
    # Преобразуем все карты в список CardReturn
    for card in cards:
        c = CardReturn(
            card_holder_name=card.card_holder_name,
            card_number=decrypt_data(card.card_number),
            exp_date=card.exp_date,
            balance=card.balance
        )
        card_list.append(c)
    
    return card_list

def update_card(user_id: int, card_id: int, card: CardUpdate):
    c = Card()
    c = Card(
        user_id=user_id,
        card_number=encrypt_data(card.card_number),
        card_holder_name=card.card_holder_name,
        exp_date=card.exp_date,
        cvv=encrypt_data(card.cvv)
    )

    return cards_repository.update_card(user_id, card_id, c)



def delete_card(user_id: int, card_id: int):
    return cards_repository.delete_card(user_id, card_id)



def get_deleted_cards(user_id):
    cards = cards_repository.get_deleted_cards(user_id)
    card_list = []
    
    for card in cards:
        c = CardReturn(
            card_holder_name=card.card_holder_name,
            card_number=decrypt_data(card.card_number),
            exp_date=card.exp_date,
            balance=card.balance
        )
        card_list.append(c)
    
    return card_list



def get_card_by_number(user_id, card_number):
    encrypted_card_number = encrypt_data(card_number)
    logger.debug(f"Encrypted card number: {encrypted_card_number}")

    card = cards_repository.get_card_by_number(user_id, encrypted_card_number)

    if card is None:
        logger.warning(f"Card not found for PAN: {card_number} and user_id: {user_id}")
        return None

    decrypted_card_number = decrypt_data(card.card_number)
    logger.info(f"Card found: {card.card_holder_name}, PAN: {decrypted_card_number}")

    c = CardReturn(
        card_holder_name=card.card_holder_name,
        card_number=decrypted_card_number,
        exp_date=card.exp_date,
        balance=card.balance
    )

    return c







    







    

