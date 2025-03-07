from pydantic import BaseModel


class UserSchema(BaseModel):
    name: str
    surname : str
    email : str
    phone : int
    password : str


class VerificationRequest(BaseModel):
    email: str  
    verification_code: str



class UserSignInSchema(BaseModel):
    phone: str
    password: str
