from pydantic import BaseModel


class MoneyTransfer(BaseModel):
    source_type: str
    source_number: int
    amount: float
    dest_type: str
    dest_number: int


