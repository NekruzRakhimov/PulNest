from pydantic import BaseModel, Field
from decimal import Decimal

class WalletBase(BaseModel):
    phone: str
    balance: float
    bonus_balance: float



class WalletTransferWallet(BaseModel):
    amount:  Decimal = Field(..., gt=0, le=Decimal("9999999999.99"), examples=["100.50"])
    receiver_wallet_number: str = Field(..., max_length=12)
    comment: str = Field(..., max_length=100)


class WalletTransferCard(BaseModel):
    amount:  Decimal = Field(..., gt=0, le=Decimal("9999999999.99"), examples=["100.50"])
    receiver_card_number: str = Field(..., min_length=16, max_length=16, pattern=r"^\d{16}$")
    comment: str = Field(..., max_length=100)