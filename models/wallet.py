from decimal import Decimal

from tortoise import models, fields, transactions
import uuid
from .transactions import Status


class Wallet(models.Model):
    """Wallet model representing a user's wallet with balance and transactions."""
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    user = fields.ForeignKeyField("models.User", related_name="wallets")
    balance = fields.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta: # type: ignore
        table = "wallet"
        # constraints = [
        #     fields.CheckConstraint(check="balance >= 0", name="check_balance_non_negative")
        # ]

    def __str__(self):
        return f"Wallet {self.id} for User {self.user.id} with Balance {self.balance}"
    
    async def calculate_balance(self) -> Decimal:
        from tortoise.functions import Sum  
        
        async with transactions.in_transaction() as connection:
            locked_wallet = await Wallet.select_for_update().using_db(connection).get(id=self.id)

            credits_sum = await locked_wallet.transactions.filter( # type: ignore
                status=Status.COMPLETED, 
                type="credit"
            ).using_db(connection).annotate(total=Sum("amount")).values_list("total", flat=True)

            debits_sum = await locked_wallet.transactions.filter( # type: ignore
                status=Status.COMPLETED, 
                type="debit"
            ).using_db(connection).annotate(total=Sum("amount")).values_list("total", flat=True)

            total_credits = Decimal(credits_sum[0] or 0)
            total_debits = Decimal(debits_sum[0] or 0)
            net_balance = total_credits - total_debits

            locked_wallet.balance = net_balance
            await locked_wallet.save(using_db=connection)
            
            self.balance = net_balance
            return self.balance