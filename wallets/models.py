import uuid
from django.db import models


class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)


class Transaction(models.Model):
    OPERATION_TYPES = (
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAW', 'Withdraw'),
    )

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    operation_type = models.CharField(max_length=10, choices=OPERATION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)





