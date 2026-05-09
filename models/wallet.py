from tortoise import models, fields
import uuid
from .transactions import Status


class Wallet(models.Model):
    """Wallet model representing a user's wallet with balance and transactions."""
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    user = fields.ForeignKeyField("models.User", related_name="wallets")
    balance = fields.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta: # type: ignore
        table = "wallet"
        # constraints = [
        #     fields.CheckConstraint("balance >= 0", name="check_balance_non_negative")
        # ]

    def __str__(self):
        return f"Wallet {self.id} for User {self.user.id} with Balance {self.balance}"
    
    def calculate_balance(self):
        transactions = self.transactions.filter( # type: ignore
            user=self.user, 
            status=Status.COMPLETED
        ).all()
        balance = 0
        for transaction in transactions:
            if transaction.type == "credit":
                balance += transaction.amount
            elif transaction.type == "debit":
                balance -= transaction.amount
        self.balance = balance
        return self.balance