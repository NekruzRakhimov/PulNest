from pydantic import BaseModel

class WalletBase(BaseModel):
    phone: str
    balance: float
    bonus_balance: float


class WalletBalanceResponse(BaseModel):
    balance: float
    bonus_balance: float

