from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Transaction
from .serializers import TransactionSerializer

import json

@api_view(["GET"])
def get_transactions_by_id(request, id):
    try:
        transaction = Transaction.objects.get(pk=id)

    except:
        return Response(status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TransactionSerializer(transaction)

        return Response(serializer.data)

    else:
        return Response(status.HTTP_400_BAD_REQUEST)