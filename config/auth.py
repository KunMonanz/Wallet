import logging

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from models.blacklist_token import BlackListedToken
from .jwt_config import SECRET_KEY, ALGORITHM
from models.users import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
logger = logging.getLogger(__name__)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # 1. Enforce strict configuration safety early (or at application startup)
    if not SECRET_KEY or not ALGORITHM:
        logger.error("SECRET_KEY or ALGORITHM environment variables are missing")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server configuration error",
        )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not isinstance(payload, dict):
            logger.error("Decoded JWT payload is not a dictionary")
            raise credentials_exception
        
        if payload.get("exp") is None:
            logger.error("JWT payload missing 'exp' claim")
            raise credentials_exception
        
        if payload.get("sub") is None:
            logger.error("JWT payload missing 'sub' claim")
            raise credentials_exception
        
        if payload.get("jti") is None:
            logger.error("JWT payload missing 'jti' claim")
            raise credentials_exception
        
        user_id: str = payload.get("sub") # type: ignore
        jti: str = payload.get("jti") # type: ignore
        
        if not user_id or not jti:
            logger.error("JWT payload missing critical claims (sub/jti)")
            raise credentials_exception
            
    except JWTError as e:
        logger.error(f"JWT decoding failed: {e}")
        raise credentials_exception
        
    if await BlackListedToken.get_or_none(jti=jti):
        logger.warning(f"Blacklisted token used for user ID: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
        )
        
    user = await User.get_or_none(id=user_id)
    if not user:
        logger.error(f"Active token presented for non-existent user ID: {user_id}")
        raise credentials_exception
    
    if not user.is_active:
        logger.warning(f"Deactivated user ID {user_id} attempted access")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, # 403 is standard for banned/deactivated accounts
            detail="Account has been deactivated",
        )
        
    return user

