import uuid
from django.db import models, transaction

class Account(models.Model):
    """
    Account model with account_id and balance
    """
    account_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    balance = models.IntegerField()

    def __str__(self):
        return f"Account {self.account_id} with Balance of {self.balance}"

class Transaction(models.Model):
    """
    Financial transaction related to Account
    """
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transactions")
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Made an transaction with Amount {self.amount} at {self.created_at}"
    
    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        with transaction.atomic():
            if self._state.adding:
                self.account.balance += self.amount
                self.account.save()
            super().save(*args)

    class Meta:
        ordering = ["-created_at"]

