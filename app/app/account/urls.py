from django.urls import path, include
from rest_framework.routers import SimpleRouter
from app.account.views import AccountViewSet, TransactionViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'accounts', AccountViewSet, basename='account')
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
]