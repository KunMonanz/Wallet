from typing import Optional
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
import logging

logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


def create_access_token(
    data: dict, 
    expires_delta: Optional[timedelta] = None
) -> str:
    if not SECRET_KEY:
        logger.error("SECRET_KEY is not set in environment variables")
        raise ValueError("SECRET_KEY is required for JWT token generation")

    if not ALGORITHM:
        logger.error("ALGORITHM is not set in environment variables")
        raise ValueError("ALGORITHM is required for JWT token generation")

    if not ACCESS_TOKEN_EXPIRE_MINUTES:
        logger.error("ACCESS_TOKEN_EXPIRE_MINUTES is not set in environment variables")
        raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES is required for JWT token generation")
    
    try:
        to_encode = data.copy()
        logger.debug(f"Creating access token with data: {to_encode} and expires_delta: {expires_delta}")
        if expires_delta:
            logger.debug(f"Attempting to create access token with custom expiration time: {expires_delta}")
            expire = datetime.utcnow() + expires_delta
            logger.debug(f"Creating access token with custom expiration time: {expire}")
        else:
            logger.debug(
                f"Creating access token with default expiration time: {ACCESS_TOKEN_EXPIRE_MINUTES} minutes")
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            logger.debug(f"Creating access token with default expiration time: {expire}")
        logger.debug(f"Creating access token with data: {to_encode} and expiration time: {expire}")
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error creating access token: {str(e)}")
        raise JWTError(f"Error creating access token: {str(e)}")