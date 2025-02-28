from pydantic import BaseModel, Field
from datetime import datetime

class CardBase(BaseModel):
    card_holder_name: str
    exp_date: str = Field(..., regex=r"^(0[1-9]|1[0-2])\/\d{2}$")  # mm/yy

class CardCreate(CardBase):
    card_number: str = Field(..., min_length=16, max_length=16, regex=r"^\d{16}$")
    cvv: str = Field(..., min_length=3, max_length=3, regex=r"^\d{3}$")

class CardUpdate(CardBase):
    card_number: str = Field(..., min_length=16, max_length=16, regex=r"^\d{16}$")
    cvv: str = Field(..., min_length=3, max_length=3, regex=r"^\d{3}$")

class CardResponse(CardBase):
    id: int
    created_at: datetime
    deleted_at: datetime | None = None

    class Config:
        from_attributes = True  # В Pydantic 2.x вместо orm_mode

class CardReturn(BaseModel):
    card_holder_name: str
    card_number: str = Field(..., min_length=16, max_length=16, regex=r"^\d{16}$")
    exp_date: str
    balance: float






