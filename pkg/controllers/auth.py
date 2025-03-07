import json
from fastapi import APIRouter, status, Depends, HTTPException, Header
from starlette.responses import Response

from logger.logger import logger
from schemas.user import UserSchema, UserSignInSchema, VerificationRequest

from pkg.services import user as user_service
from utils.auth import create_access_token

router = APIRouter()


@router.post('/sign-up', summary='Sign up in app', tags=["auth"])
def sign_up(user: UserSchema):
    # Check if user with the same phone or email already exists
    user_db_phone = user_service.get_user_by_phone(user.phone)
    user_db_email = user_service.get_user_by_email(user.email)

    if user_db_phone is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this phone already exists"
        )
    
    if user_db_email is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # Create the user in the database
    user_service.create_user(user)

    return {
        "message": "User registered successfully. Please verify your email."
    }


@router.post('/send-verification-code', summary='Send verification code to email', tags=["auth"])
def send_verification(email: str):
    # Check if the user exists
    user = user_service.get_user_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email does not exist"
        )

    # Send verification code to the user's email
    code = user_service.send_verification_email(email)

    return {
        "message": "Verification code sent successfully"
    }


@router.post('/verify-email', summary='Verify user email', tags=["auth"])
def verify_user(verification_request: VerificationRequest):
    # Verify the user
    if user_service.verify_user(verification_request.email, verification_request.verification_code):
        return {
            "message": "User verified successfully"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired code"
        )


@router.post('/sign-in', summary='Sign in to app', tags=["auth"])
def sign_in(user: UserSignInSchema):
    user_from_db = user_service.get_user_by_phone_and_password(user.phone, user.password)
    if user_from_db is None:

        return Response(json.dumps({'error': 'Wrong login or password'}), status.HTTP_404_NOT_FOUND)

    elif not user_from_db.is_verified:

        return Response(json.dumps({'message' : 'Please verify your email.'}), status.HTTP_401_UNAUTHORIZED)

    # Создаем JWT токен
    access_token = create_access_token(
        data={
            "id": user_from_db.id
        }
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

