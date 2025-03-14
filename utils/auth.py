import jwt
import datetime
from typing import Optional
from fastapi import status, HTTPException
from pydantic import BaseModel

from configs.config import settings


# Модель данных для полезной нагрузки токена
class TokenPayload(BaseModel):
    id: int
    role : str
    exp: datetime.datetime


# Функция для создания JWT токена
def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    to_encode = data.copy()

    # Получаем текущее время в UTC
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
            minutes=settings.auth.access_token_expire_minutes)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.auth.secret_key, algorithm=settings.auth.algorithm)
    return encoded_jwt


# Функция для верификации JWT токена
def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.auth.secret_key, algorithms=[settings.auth.algorithm])
        return TokenPayload(**payload)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
