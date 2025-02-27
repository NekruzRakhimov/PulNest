from db.models import Cards
from pkg.repositories import cards as cards_repository
from schemas.cards import CardCreate, CardUpdate, CardResponse, CardReturn


cipher_suite = Fernet(b"our-key-here")
def encrypt_data(self, data: str) -> str:
        return self.cipher_suite.encrypt(data.encode()).decode()

def decrypt_data(self, data: str) -> str:
        return self.cipher_suite.decrypt(data.encode()).decode()

def add_card(user_id, card: CardCreate):
        encrypted_card_number = encrypt_data(card.card_number)
        encrypted_cvv = encrypt_data(card.cvv)
        c = Cards()
        c.user_id = 1,
        c.card_number = encrypted_card_number,
        c.card_holder_name = card.card_holder_name,
        c.exp_date = card.exp_date,
        c.cvv = encrypted_cvv
        return cards_repository.add_card(c)


def get_card_by_id(user_id, card_id):
    card = cards_repository.get_card_by_id(user_id, card_id)
    c = CardReturn()
    c.card_holder_name = card.card_holder_name,
    c.card_number = card.card_number,
    c.exp_date = card.exp_date
    c.balance = card.balance
    return card
    
def get_all_cards(user_id):
    cards = cards_repository.get_all_cards(user_id)
    card_list = list()
    for card in cards:
        c = CardReturn()
        c.card_holder_name = card.card_holder_name,
        c.card_number = card.card_number,
        c.exp_date = card.exp_date
        c.balance = card.balance
        card_list.append(c)
    return card_list
   







    # def get_card(self, card_id: int) -> CardResponse:
    #     card = self.repository.get_card(card_id)
    #     if not card:
    #         raise Exception("Card not found")
    #     # Дешифруем PAN и CVV перед возвратом
    #     card.card_number = self.decrypt_data(card.card_number)
    #     card.cvv = self.decrypt_data(card.cvv)
    #     return CardResponse(**card)

    # def update_card(self, card_id: int, card: CardUpdate) -> CardResponse:
    #     # Шифруем PAN и CVV перед обновлением
    #     encrypted_card_number = self.encrypt_data(card.card_number)
    #     encrypted_cvv = self.encrypt_data(card.cvv)
    #     card_data = self.repository.update_card(
    #         card_id=card_id,
    #         card_number=encrypted_card_number,
    #         card_holder_name=card.card_holder_name,
    #         exp_date=card.exp_date,
    #         cvv=encrypted_cvv
    #     )
    #     return CardResponse(**card_data)

    # def delete_card(self, card_id: int):
    #     card = self.repository.get_card(card_id)
    #     if not card:
    #         raise Exception("Card not found")
    #     self.repository.delete_card(card_id)
