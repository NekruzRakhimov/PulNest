from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal

class CardBase(BaseModel):
    card_holder_name: str
    exp_date: str = Field(..., pattern=r"^(0[1-9]|1[0-2])\/\d{2}$")  # mm/yy



class CardCreate(CardBase):
    card_number: str = Field(..., min_length=16, max_length=16, pattern=r"^\d{16}$")
    cvv: str = Field(..., min_length=3, max_length=3, pattern=r"^\d{3}$")



class CardUpdate(CardBase):
    card_number: str = Field(..., min_length=16, max_length=16, pattern=r"^\d{16}$")
    cvv: str = Field(..., min_length=3, max_length=3, pattern=r"^\d{3}$")



class CardResponse(CardBase):
    id: int
    created_at: datetime
    deleted_at: datetime | None = None

    class Config:
        from_attributes = True  # Pydantic 2.x



class CardReturn(BaseModel):
    id: int
    card_holder_name: str
    card_number: str = Field(..., min_length=16, max_length=16, pattern=r"^\d{16}$")
    exp_date: str
    balance: float



class CardTransferCard(BaseModel):
    sender_card_number: str = Field(..., min_length=16, max_length=16, pattern=r"^\d{16}$")
    amount: Decimal = Field(..., gt=0, le=Decimal("9999999999.99"), examples=["100.50"])
    receiver_card_number: str = Field(..., min_length=16, max_length=16, pattern=r"^\d{16}$")






