from pydantic import BaseModel
from decimal import Decimal

class HistoryTransaction(BaseModel):
    id: int
    source_type: str
    source_id: int
    source_number: str
    amount: float
    dest_type: str
    dest_id: int
    dest_number: str
    status: str
    created_at: str 





