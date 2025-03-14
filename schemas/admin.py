from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AdminSchema(BaseModel):
    name: str
    surname: str
    email: str
    password: str
 

class AdminSignInSchema(BaseModel):
    email: str
    password: str