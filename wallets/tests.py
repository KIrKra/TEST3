from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Wallet
import uuid
import threading


class WalletTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.wallet = Wallet.objects.create(balance=1000.00)
        self.wallet_url = f'/api/v1/wallets/{self.wallet.id}'
        self.operation_url = f'{self.wallet_url}/operation'

    def test_get_balance(self):
        response = self.client.get(self.wallet_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance'], 1000.00)

    def test_deposit(self):
        data = {'operation_type': 'DEPOSIT', 'amount': 500}
        response = self.client.post(self.operation_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance'], 1500.00)

    def test_withdraw(self):
        data = {'operation_type': 'WITHDRAW', 'amount': 500}
        response = self.client.post(self.operation_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance'], 500.00)

    def test_insufficient_funds(self):
        data = {'operation_type': 'WITHDRAW', 'amount': 1500}
        response = self.client.post(self.operation_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_concurrent_requests(self):
        def perform_operation():
            client = APIClient()
            data = {'operation_type': 'WITHDRAW', 'amount': 100}
            client.post(self.operation_url, data, format='json')

        threads = []
        for _ in range(5):
            t = threading.Thread(target=perform_operation)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        wallet = Wallet.objects.get(id=self.wallet.id)
        self.assertEqual(float(wallet.balance), 500.00)