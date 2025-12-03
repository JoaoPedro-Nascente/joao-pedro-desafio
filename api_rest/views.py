from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Transaction
from .serializers import TransactionSerializer

import json

#It's a very simple function, but it can be easily modified to become more complex in the future
def get_transaction_by_id(transaction):
    serializer = TransactionSerializer(transaction)
    return Response(serializer.data, status=status.HTTP_200_OK)


def update_transaction(data, transaction):
    serializer = TransactionSerializer(transaction, data=data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

def delete_transaction(transaction):
    transaction.delete()
    return Response(status.HTTP_204_NO_CONTENT)
    

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def transactions_manager(request, id):
    try:
        transaction = Transaction.objects.get(pk=id)
        
    except:
        return Response(status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return get_transaction_by_id(transaction)

    
    if (request.method == 'PUT') or (request.method == 'PATCH'):
        return update_transaction(request.data, transaction)

    if request.method == 'DELETE':
        return delete_transaction(transaction)

    #If no method is valid
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