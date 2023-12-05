from rest_framework import routers
from .views import ProfileViewSet, UserViewSet, TransactionViewSet, AddBalanceViewSet

router = routers.DefaultRouter()
router.register('profiles/', ProfileViewSet, basename='profiles')
router.register('users/', UserViewSet, basename='users')
router.register('transactions/', TransactionViewSet, basename='transactions')
router.register('addbalance/', AddBalanceViewSet, basename='addbalance')

urlpatterns = router.urls