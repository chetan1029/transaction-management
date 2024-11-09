import uuid
from rest_framework.test import APITestCase
from rest_framework.exceptions import ValidationError
from app.account.models import Account, Transaction
from app.account.serializers import TransactionSerializers

class TransactionSerializerTest(APITestCase):

    def setUp(self):
        # Create a sample account to use in tests
        self.existing_account = Account.objects.create(account_id=uuid.uuid4(), balance=100)

    def test_invalid_uuid_for_account_id(self):
        """
        Test that an invalid UUID raises a validation error.
        """
        data = {
            "account_id": 12345,  # Invalid UUID format
            "amount": 50
        }
        serializer = TransactionSerializers(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_account_creation_if_not_exists(self):
        """
        Test that a new account is created if the account_id does not exist.
        """
        new_account_id = str(uuid.uuid4())  # Generate a new UUID
        data = {
            "account_id": new_account_id,
            "amount": 50
        }
        serializer = TransactionSerializers(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        new_account = Account.objects.get(account_id=new_account_id)
        self.assertEqual(new_account.balance, 50, "Newly created account should have an initial balance updated by the transaction amount.")

    def test_transaction_updates_account_balance(self):
        """
        Test that creating a transaction updates the account balance.
        """
        initial_balance = self.existing_account.balance
        data = {
            "account_id": str(self.existing_account.account_id),
            "amount": 25
        }
        serializer = TransactionSerializers(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.existing_account.refresh_from_db()
        self.assertEqual(self.existing_account.balance, initial_balance + 25, "Account balance should be updated by the transaction amount.")

    def test_transaction_creation_returns_transaction_object(self):
        """
        Test that the transaction creation.
        """
        data = {
            "account_id": str(self.existing_account.account_id),
            "amount": 20
        }
        serializer = TransactionSerializers(data=data)
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save()

        self.assertEqual(transaction.amount, 20)
        self.assertEqual(transaction.account.account_id, self.existing_account.account_id)
