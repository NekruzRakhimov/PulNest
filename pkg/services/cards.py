from db.models import Card
from pkg.repositories import cards as cards_repository
from schemas.cards import CardCreate, CardReturn, CardUpdate
# from cryptography.fernet import Fernet
from logger.logger import logger

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# Фиксированный 16-байтовый ключ (AES требует ключ длиной 16, 24 или 32 байта)
KEY = b'YourSecretKey123'  # Длина ключа должна быть ровно 16 байт


def encrypt_data(text: str) -> str:
    cipher = AES.new(KEY, AES.MODE_ECB)
    encrypted_bytes = cipher.encrypt(pad(text.encode(), AES.block_size))
    return base64.b64encode(encrypted_bytes).decode()


def decrypt_data(encrypted_text: str) -> str:
    cipher = AES.new(KEY, AES.MODE_ECB)
    decrypted_bytes = unpad(cipher.decrypt(base64.b64decode(encrypted_text)), AES.block_size)
    return decrypted_bytes.decode()

def add_card(user_id, card: CardCreate):
    encrypted_card_number = encrypt_data(card.card_number)
    encrypted_cvv = encrypt_data(card.cvv)
    
    logger.info(encrypt_data(card.card_number))
    logger.info(encrypt_data(card.card_number))

    c = Card(
        user_id=user_id,
        card_number=encrypted_card_number,
        card_holder_name=card.card_holder_name,
        exp_date=card.exp_date,
        cvv=encrypted_cvv
    )
    
    logger.info(f"Adding card: user_id={user_id}, card_number=****{encrypted_card_number[-4:]}, cvv=***")
    return cards_repository.add_card(user_id, c)




def get_card_by_id(user_id, card_id):
    card = cards_repository.get_card_by_id(user_id, card_id)
    if card is None:
        return None
    
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



def get_card_by_card_number(user_id, card_number):
    encrypted_card_number = encrypt_data(card_number)
    logger.info("Encrypted card number:" + encrypted_card_number)

    card = cards_repository.get_card_by_card_number(user_id, encrypted_card_number)

    if card is None:
        logger.info(f"Card not found for PAN: {card_number} and user_id: {user_id}")
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













    







    

