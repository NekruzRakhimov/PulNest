from pydantic import BaseModel, constr
from datetime import datetime



from pydantic import BaseModel, Field

class CardBase(BaseModel):
    user_id: int
    card_holder_name: str
    exp_date: str = Field(..., regex=r"^(0[1-9]|1[0-2])\/\d{2}$")  # Валидация формата mm/yy


class CardCreate(CardBase):
    card_number: str
    cvv: str

class CardUpdate(CardBase):
    card_number: str
    cvv: str

class CardResponse(CardBase):
    id: int
    created_at: datetime
    deleted_at: datetime

    class Config:
        orm_mode = True

class CardReturn():
    card_holder_name: str
    card_number: str
    exp_date: str
    balance: float





