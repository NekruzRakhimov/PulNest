from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, field_validator



class CardBase(BaseModel):
    card_holder_name: str
    exp_date: str = Field(..., pattern=r"^(0[1-9]|1[0-2])\/\d{2}$") # mm/yy

    @field_validator('exp_date')
    def check_expiration_date(cls, v):
        # Преобразуем строку в формат MM/YY в объект datetime
        exp_date = datetime.strptime(v, "%m/%y")
        current_date = datetime.now()

        # Проверяем, что дата истечения не меньше текущей
        if exp_date < current_date:
            raise ValueError("Expiration date must be in the future")
        return v



class CardCreate(CardBase):
    card_number: str = Field(..., min_length=16, max_length=16, pattern=r"^\d{16}$")
    cvv: str = Field(..., min_length=3, max_length=3, pattern=r"^\d{3}$")



class CardUpdate(CardBase):
    card_number: str = Field(..., min_length=16, max_length=16, pattern=r"^\d{16}$")
    cvv: str = Field(..., min_length=3, max_length=3, pattern=r"^\d{3}$")



class CardResponse(CardBase):
    id: int
    created_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Pydantic 2.x



class CardReturn(BaseModel):
    user_id: int
    id: int
    card_holder_name: str
    card_number: str = Field(..., min_length=16, max_length=16, pattern=r"^\d{16}$")
    exp_date: str
    balance: float



class CardTransferCard(BaseModel):
    sender_card_number: str = Field(..., min_length=16, max_length=16, pattern=r"^\d{16}$")
    amount: Decimal = Field(..., gt=0, le=Decimal("9999999999.99"), examples=["100.50"])
    receiver_card_number: str = Field(..., min_length=16, max_length=16, pattern=r"^\d{16}$")
    comment: str = Field(..., max_length=100)



class CardTransferWallet(BaseModel):
    sender_card_number: str = Field(..., min_length=16, max_length=16, pattern=r"^\d{16}$")
    amount: Decimal = Field(..., gt=0, le=Decimal("9999999999.99"), examples=["100.50"])
    receiver_wallet_number: str = Field(..., max_length=12)
    comment: str = Field(..., max_length=100)




