from pydantic import BaseModel, constr, EmailStr
from datetime import date


class UserSchema(BaseModel):
    name : str
    surname : str
    birth_date : str
    email : EmailStr
    phone : constr(min_length=12, max_length=12)
    password : str


class VerificationRequest(BaseModel):
    email: str  
    verification_code: str



class UserSignInSchema(BaseModel):
    phone: constr(min_length=12, max_length=12)
    password: str
