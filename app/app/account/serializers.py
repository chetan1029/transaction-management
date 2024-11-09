import uuid
from django.core.exceptions import ObjectDoesNotExist

from app.account.models import Account, Transaction
from rest_framework import serializers

class AccountSerializers(serializers.ModelSerializer):
    """
    Account Serializers to serialize Account Model
    """
    class Meta:
        model = Account
        fields = ["account_id", "balance"]

class TransactionSerializers(serializers.ModelSerializer):
    """
    Transaction Serializers
    """
    account_id = serializers.CharField()

    class Meta:
        model = Transaction
        fields = ["transaction_id", "account_id", "amount", "created_at"]
        read_only_fields = ["transaction_id", "created_at"]

    def validate_account_id(self, account_id):
        # check if its string
        print(account_id)
        try:
            # This will raise a ValueError if `value` is not a valid UUID string
            uuid.UUID(account_id, version=4)
        except (ValueError, TypeError):
            raise serializers.ValidationError("account_id must be a valid UUID string.")

        # Check if the account exists, create if not
        try:
            Account.objects.get(account_id=account_id)
        except ObjectDoesNotExist:
            Account.objects.create(account_id=account_id, balance=0)
        return account_id

    def create(self, validated_data):
        account_id = validated_data.pop('account_id')
        amount = validated_data.get('amount')

        # Fetch the account object using the account_id
        account = Account.objects.get(account_id=account_id)

        # Update account balance
        account.balance += amount
        account.save()

        validated_data['account'] = account
        return super().create(validated_data)