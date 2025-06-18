from django.shortcuts import render
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Wallet, Transaction


class WalletDetail(APIView):
    def get(self, request, wallet_uuid):
        wallet = get_object_or_404(Wallet, id=wallet_uuid)
        return Response({'balance': float(wallet.balance)})


class WalletOperation(APIView):
    def post(self, request, wallet_uuid):
        operation_type = request.data.get('operation_type')
        amount = request.data.get('amount')

        if not operation_type or not amount:
            return Response({'error': 'Missing parameters'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except (TypeError, ValueError):
            return Response({'error': 'Invalid amount'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                wallet = Wallet.objects.select_for_update().get(id=wallet_uuid)

                if operation_type == 'DEPOSIT':
                    wallet.balance += amount
                elif operation_type == 'WITHDRAW':
                    if wallet.balance < amount:
                        return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)
                    wallet.balance -= amount
                else:
                    return Response({'error': 'Invalid operation type'}, status=status.HTTP_400_BAD_REQUEST)

                wallet.save()
                Transaction.objects.create(
                    wallet=wallet,
                    operation_type=operation_type,
                    amount=amount
                )

                return Response({'balance': float(wallet.balance)})

        except Wallet.DoesNotExist:
            return Response({'error': 'Wallet not found'}, status=status.HTTP_404_NOT_FOUND)