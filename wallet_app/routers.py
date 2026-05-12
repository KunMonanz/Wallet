from fastapi import APIRouter, Depends, HTTPException, status

from config.auth import get_current_user
from wallet_app.wallet_crud import WalletRepository


router = APIRouter(
    prefix="/api/v1/wallets",
    tags=["wallets"],
)

@router.get("/me")
async def get_my_wallet(current_user=Depends(get_current_user)):
    """Endpoint to get the current user's wallet."""
    wallet = await WalletRepository.get_wallet_by_user_id(current_user.id)
    return wallet


@router.get("/balance")
async def get_balance(current_user=Depends(get_current_user)):
    """Endpoint to get the current user's wallet balance."""
    wallet = await WalletRepository.get_wallet_by_user_id(current_user.id)
    balance = await wallet.calculate_balance()
    return {"balance": balance}
    