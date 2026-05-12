from decimal import Decimal

from models import Wallet, Transaction
from models.users import User


class WalletRepository:
    
    @staticmethod
    async def create_wallet(user_id: str) -> Wallet:
        """Create a new wallet for a user."""
        wallet = await Wallet.create(user_id=user_id)
        await wallet.save()
        return wallet
    
    @staticmethod
    async def get_wallet_by_id(wallet_id: str) -> Wallet:
        """Get a wallet by its ID."""
        wallet = await Wallet.get_or_none(id=wallet_id).select_related("user")
        if not wallet:
            wallet = await WalletRepository.create_wallet(user_id=wallet_id)
            return wallet
        return wallet
    
    @staticmethod
    async def get_wallet_by_user_id(user_id: str) -> Wallet:
        """Get a wallet by the user ID."""
        wallet = await Wallet.get_or_none(user_id=user_id).select_related("user")
        if not wallet:
            wallet = await WalletRepository.create_wallet(user_id=user_id)
            return wallet
        return wallet
    
    @staticmethod
    async def get_wallet_by_user_email(user: User) -> Wallet|None:
        """Get a wallet by the user's email."""
        wallet = await Wallet.get_or_none(user__email=user.email).select_related("user")
        if not wallet:
            wallet = await WalletRepository.create_wallet(user_id=user.id)
            return wallet
        return wallet
    
    @staticmethod
    async def get_wallet_balance(wallet_id: str) -> Decimal|int:
        """Get the balance of a wallet."""
        wallet = await Wallet.get_or_none(id=wallet_id).select_related("user")
        if wallet is None:
            wallet = await WalletRepository.create_wallet(user_id=wallet_id)
            return wallet.balance
        return wallet.balance

    