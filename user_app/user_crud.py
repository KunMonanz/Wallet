import uuid

from models.users import User
from config.password_config import hash_password, verify_password

class UserRepository:
    """Repository for performing CRUD operations on User model."""
    
    @staticmethod
    async def create_user(username: str, email: str, password: str) -> User:
        """Create a new user."""
        hashed_password = hash_password(password)
        user = await User.create(
            username=username, 
            email=email, 
            password_hash=hashed_password
        )
        return user

    @staticmethod
    async def get_user_by_id(user_id: uuid.UUID) -> User|None:
        """Get a user by their ID."""
        user = await User.get_or_none(id=user_id)
        return user

    @staticmethod
    async def get_user_by_email(email: str) -> User|None:
        """Get a user by their email."""
        user = await User.get_or_none(email=email)
        return user

    @staticmethod
    async def get_user_by_username(username: str) -> User|None:
        """Get a user by their username."""
        user = await User.get_or_none(username=username)
        return user

    @staticmethod
    async def get_user_by_username_or_email(entry: str) -> User|None:
        """Get a user by their username or email."""
        user = await User.get_or_none(username=entry) or await User.get_or_none(email=entry)
        return user
    
    @staticmethod
    async def update_user(user_id: uuid.UUID, **kwargs) -> User:
        """Update a user's information."""
        await User.filter(id=user_id).update(**kwargs)
        updated_user = await User.get(id=user_id)
        return updated_user

    @staticmethod
    async def delete_user(user_id: uuid.UUID) -> None:
        """Delete a user by their ID."""
        await User.filter(id=user_id).delete()