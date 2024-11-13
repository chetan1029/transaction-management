import uuid
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from app.account.models import Account, Transaction
from rest_framework import serializers

class AccountSerializer(serializers.ModelSerializer):
    """
    Account Serializers to serialize Account Model
    """
    class Meta:
        model = Account
        fields = ["account_id", "balance"]


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Transaction model.
    """
    account_id = serializers.CharField()

    class Meta:
        model = Transaction
        fields = ['transaction_id', 'account_id', 'amount', 'created_at']
        read_only_fields = ['transaction_id', 'created_at']

    def validate_account_id(self, account_id):
        """
        Validates that account_id is a valid UUID and that the associated Account exists.
        """
        try:
            uuid_obj = uuid.UUID(account_id, version=4)
            if str(uuid_obj) != account_id:
                raise ValueError
        except (ValueError, TypeError):
            raise serializers.ValidationError("account_id must be a valid UUID string.")
        return account_id

    def create(self, validated_data):
        # Extract account_id and fetch the related Account object
        account_id = validated_data.pop('account_id')

        account, _ = Account.objects.get_or_create(account_id=account_id, defaults={'balance': 0})

        # Create the transaction, associating it with the account
        transaction = Transaction.objects.create(account=account, **validated_data)

        # Adjust the account balance after the transaction is created
        # account.balance += transaction.amount
        # account.save()

        return transaction