from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Transaction
from .serializers import TransactionSerializer

import json

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def transactions_manager(request, id):
    if request.method == 'GET':
        try:
            transaction = Transaction.objects.get(pk=id)

            serializer = TransactionSerializer(transaction)
            return Response(serializer.data)
        
        except:
            return Response(status.HTTP_404_NOT_FOUND)
    
    if (request.method == 'PUT') or (request.method == 'PATCH'):
        try:
            updated_transaction = Transaction.objects.get(pk=id)
        except:
            return Response(status.HTTP_404_NOT_FOUND)
        
        is_partial = request.method == 'PATCH'
        serializer = TransactionSerializer(updated_transaction, data=request.data, partial=is_partial)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_new_transaction(request):
    if request.method == 'POST':
        new_transaction = request.data

        serializer = TransactionSerializer(data=new_transaction)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(status.HTTP_400_BAD_REQUEST)