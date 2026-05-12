import uuid

from fastapi import APIRouter, HTTPException, Request, status, Depends
from fastapi.responses import JSONResponse

from config.jwt_config import create_access_token, decode_token
from config.password_config import verify_password
from config.auth import get_current_user

from models.blacklist_token import BlackListedToken
from .services import get_jwt_from_headers


from .schema import (
    UserCreate, 
    UserLogin, 
    UserResponse,
    EmailToken,
)

from .user_crud import UserRepository

from .utils.email_utils import decode_email_token

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
)


@router.post("/register", response_model=UserResponse)
async def create_user(user_create: UserCreate):
    """Endpoint to create a new user."""
    if await UserRepository.get_user_by_username_or_email(user_create.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Account already exists"
        )
        
    username = user_create.username.strip().lower()
    email = user_create.email.strip().lower()
    
    user = await UserRepository.create_user(
        username=username, 
        email=email, 
        password=user_create.password
    )
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User creation failed"
        )
    return user


@router.post("/login")
async def login(user_login: UserLogin):
    """Endpoint to log in a user."""
    entry = user_login.username_or_email.strip().lower()
    
    user = await UserRepository.get_user_by_username_or_email(
        entry
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account has be deactivated"
        )
    if not verify_password(user_login.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid password"
        )
    user_payload = {
        "sub": str(user.id),
        "jti": str(uuid.uuid4())
    }
    access_token = await create_access_token(user_payload)
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }


@router.post("/logout")
async def logout(request: Request):
    raw_jwt = get_jwt_from_headers(request)
    payload = await decode_token(raw_jwt)
    jti = payload.get("jti")
    if not jti:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token"
        )
    await UserRepository.blacklist_token(jti)
    

@router.post("/verify-email/")
async def verify_email(token: str):
    email = await decode_email_token(token)
    user_exists = await UserRepository.get_user_by_email(email)
    
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid token"
        )
        
    await UserRepository.update_user(
        user_id=user_exists.id, 
        is_email_verified=True
    )
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": "Email verified successfully"
        }
    )

    
@router.get("/username")
async def get_username(current_user=Depends(get_current_user)):
    return{
        "message": f"{current_user.email}"
    }