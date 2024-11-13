from rest_framework import viewsets, status, mixins

from app.account.models import Account, Transaction
from app.account.serializers import AccountSerializer, TransactionSerializer

class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Fetch Account detail (account_id and balance) by account_id
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class TransactionViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    """
    Listing and creating transactions
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

