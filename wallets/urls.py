from django.urls import path
from .views import WalletDetail, WalletOperation

urlpatterns = [
    path('api/v1/wallets/<uuid:wallet_uuid>', WalletDetail.as_view()),
    path('api/v1/wallets/<uuid:wallet_uuid>/operation', WalletOperation.as_view()),
]