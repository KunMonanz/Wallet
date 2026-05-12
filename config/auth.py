import logging

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from models.blacklist_token import BlackListedToken
from .jwt_config import SECRET_KEY, ALGORITHM
from models.users import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
logger = logging.getLogger(__name__)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not token:
        raise credentials_exception
    
    if not SECRET_KEY or not ALGORITHM:
        logger.error("SECRET_KEY and ALGORITHM must be set in environment variables")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server configuration error: SECRET_KEY and ALGORITHM must be set",
        )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        if payload is None:
            logger.error("JWT decode returned None payload")
            raise credentials_exception
        user_id: str = payload.get("sub") # type: ignore
        
        if user_id is None:
            logger.error("User ID not found in JWT payload")
            raise credentials_exception
        
        jti = payload.get("jti")
        if BlackListedToken.get_or_none(jti=jti):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been blacklisted"
            )
            
    except JWTError as e:
        logger.error(f"JWT decoding error: {e}")
        raise credentials_exception
        
    user = await User.get_or_none(id=user_id)
    if user is None:
        logger.error(f"User with ID {user_id} not found")
        raise credentials_exception
    
    if not user.is_active:
        logger.error(f"User with ID {user_id} attempted to use protected endpoint while deactivated")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account has be deactivated"
        )
        
    return user
