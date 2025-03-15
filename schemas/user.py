from pydantic import BaseModel, constr, EmailStr,  field_validator, ValidationError
from typing_extensions import Annotated
from datetime import date


class UserSchema(BaseModel):
    name : str
    surname : str
    birth_date : str
    email : EmailStr
    phone : constr(min_length=12, max_length=12)
    password : str

    @field_validator('phone')
    def validate_phone(cls, value):
        if not value.isdigit():
            raise ValueError('Phone number must contain only digits')
        if not value.startswith('992'):
            raise ValueError('Phone number must start with 992')
        return value



class VerificationRequest(BaseModel):
    email: str  
    verification_code: str



class UserSignInSchema(BaseModel):
    phone: Annotated[str, constr(min_length=12, max_length=12)]
    password: str