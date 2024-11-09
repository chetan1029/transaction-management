import uuid
from django.db import models

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
        return f"Made an transaction {self.transaction_id} with Amount {self.amount} on Account {self.account.account_id} at {self.created_at}"

