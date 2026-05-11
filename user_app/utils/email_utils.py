import os
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, NameEmail
from pydantic import EmailStr


FRONT_END_URL = os.getenv("FRONT_END_URL", "http://localhost:8000")
EMAIL_VERIFICATION_SECRET_KEY = os.getenv("EMAIL_VERIFICATION_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES = int(os.getenv("EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES", 60))


def create_email_verification_token(email: str) -> str:
    if not EMAIL_VERIFICATION_SECRET_KEY:
        raise ValueError(
            "EMAIL_VERIFICATION_SECRET_KEY is required for email verification token generation")
    
    if not ALGORITHM:
        raise ValueError("ALGORITHM is required for email verification token generation")
    
    if not EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES:
        raise ValueError(
            "EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES is required for email verification token generation")
    
    to_encode = {"sub": email}
    expire = datetime.utcnow() + timedelta(minutes=EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire}) # type: ignore
    encoded_jwt = jwt.encode(to_encode, EMAIL_VERIFICATION_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def send_email_verification(email: NameEmail, token: str) -> None:
    # Placeholder for email sending logic
    message = MessageSchema(
        subject="Email Verification",
        recipients=[email],
        body=f"Click the link to verify your email: {FRONT_END_URL}/verify-email?token={token}",
        subtype="html" # type: ignore
    )
    
    if not os.getenv("MAIL_USERNAME") or not os.getenv("MAIL_PASSWORD") or not os.getenv("MAIL_FROM") or not os.getenv("MAIL_PORT") or not os.getenv("MAIL_SERVER"):
        raise ValueError("Mail configuration environment variables are required for sending email")
    
    fm = FastMail(ConnectionConfig(
        MAIL_SSL_TLS=True,
        MAIL_STARTTLS=False,
        MAIL_USERNAME=os.getenv("MAIL_USERNAME"), # type: ignore
        MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"), # type: ignore
        MAIL_FROM=os.getenv("MAIL_FROM"), # type: ignore
        MAIL_PORT=int(os.getenv("MAIL_PORT")), # type: ignore
        MAIL_SERVER=os.getenv("MAIL_SERVER"), # type: ignore
    ))
    await fm.send_message(message)
    
    
async def decode_email_token(token: str) -> str:
    """Function to decode email verification token and return the user email"""
    if not EMAIL_VERIFICATION_SECRET_KEY:
        raise ValueError("EMAIL_VERIFICATION_SECRET_KEY is required for email verification token generation")
    
    if not ALGORITHM:
        raise ValueError("ALGORITHM is required for email verification token generation")
    
    payload = jwt.decode(
        token,
        EMAIL_VERIFICATION_SECRET_KEY,
        algorithms=[ALGORITHM]
    )
    
    return payload["sub"]