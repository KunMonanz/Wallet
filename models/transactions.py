from tortoise import models, fields
from enum import Enum
import uuid


class Status(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class Type(str, Enum):
    CREDIT = "credit"
    DEBIT = "debit"


class Transaction(models.Model):
    """Transaction model representing a financial transaction linked to a wallet."""
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    wallet = fields.ForeignKeyField("models.Wallet", related_name="transactions")
    amount = fields.DecimalField(max_digits=12, decimal_places=2)
    type = fields.CharEnumField(Type)
    status = fields.CharEnumField(Status, default=Status.PENDING)
    description = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    class Meta: # type: ignore
        table = "transaction"
        # constraints = [
        #     models.CheckConstraint("amount > 0", name="check_amount_positive"),
        #     fields.CheckConstraint("type IN ('credit', 'debit')", name="check_type_valid"),
        #     fields.CheckConstraint("status IN ('pending', 'completed', 'failed')", name="check_status_valid")
        # ]
    
    def __str__(self):
        return f"Transaction {self.id} of {self.amount} ({self.type}) for Wallet {self.wallet.id}"
    
    