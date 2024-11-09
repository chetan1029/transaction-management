from django.urls import path, include
from rest_framework.routers import SimpleRouter
from app.account.views import AccountViewSet, TransactionViewSet

# Custom class to remove the trailing slash
class NoSlashRouter(SimpleRouter):
    def __init__(self):
        super().__init__()
        self.trailing_slash = '/?'

router = NoSlashRouter()
router.register(r'accounts', AccountViewSet, basename='account')
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
]