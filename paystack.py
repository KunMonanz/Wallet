import requests

from settings import PAYSTACK_SECRET_KEY


def header():
    return {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }

def initialize_transaction(amount: int, email: str)-> dict:
    if amount <= 0:
        raise ValueError("Amount must be greater than zero")
    if amount < 1000:
        raise ValueError("Amount must be at least 1000 kobo (10 Naira)")
    if not email:
        raise ValueError("Email is required for initializing transaction")
    
    response = requests.post(
        url="https://api.paystack.co/transaction/initialize", 
        headers=header(), 
        json={"amount": amount, "email": email}
    )
    
    return response.json()
    