from pydantic import BaseModel, Field
from typing import Optional


class TransactionSchema(BaseModel):
    user_id: int
    tran_type: str  # income, expense
    source_type: str
    source_id: int
    source_number: str
    amount: float
    dest_type: str
    dest_id: int
    dest_number: str
    comment: Optional[str] = None
    correlation_id: Optional[int] = None
    status: str


class WalletPaymentSchema(BaseModel):
    service_id: int
    account_number : str
    amount: float
    comment: Optional[str] = None


class CardPaymentSchema(BaseModel):
    card_number: str = Field(..., min_length=16, max_length=16, pattern=r"^\d{16}$")
    service_id: int
    account_number: str
    amount: float
    comment: Optional[str] = None