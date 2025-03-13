from pydantic import BaseModel
from datetime import datetime
from typing  import Optional


class ServiceSchema(BaseModel):
    provider_name: str  
    category_id: int 



class ServiceResponse(BaseModel):
    id: int
    provider_name: str
    category_name: str

