from fastapi import APIRouter, HTTPException, status

from config.jwt_config import create_access_token
from config.password_config import verify_password

from .schema import (
    UserCreate, 
    UserLogin, 
    UserResponse,
    EmailToken,
)

from .user_crud import UserRepository
from .utils.email_utils import decode_email_token

router = APIRouter(
    prefix="/users/v1",
    tags=["users"],
)

user_repository = UserRepository()

@router.post("/register", response_model=UserResponse)
async def create_user(user_create: UserCreate):
    """Endpoint to create a new user."""
    if await user_repository.get_user_by_username_or_email(user_create.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Account already exists"
        )
        
    username = user_create.username.strip().lower()
    email = user_create.email.strip().lower()
    
    user = await user_repository.create_user(
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
    
    user = await user_repository.get_user_by_username_or_email(
        entry
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    if not user.is_active:
        
    if not verify_password(user_login.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid password"
        )
    user_payload = {
        "sub": str(user.id),
    }
    access_token = create_access_token(user_payload)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/verify-email/")
async def verify_email(token: str):
    email = await decode_email_token(token)
    user_exists = await user_repository.get_user_by_email(email)
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid token"
        )
    user_exists.is_email_verified = True
    await user_exists.save()
    
