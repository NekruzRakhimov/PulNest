from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ServiceSchema(BaseModel):
    merchant_name: str  
    category_id: int 


class ServiceResponse(BaseModel):
    id: int
    merchant_name: str
    category_id: int

