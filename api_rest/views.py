from django.shortcuts import render

from django.db.models import Sum, DecimalField, Q

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Transaction
from .models import TypeTransaction
from .serializers import TransactionSerializer
from .serializers import SummarySerializer
from .pagination import StandardResultsSetPagination

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


def create_new_transaction(data):
    new_transaction = data

    serializer = TransactionSerializer(data=new_transaction)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

def get_filtered_transactions(query_params):
    transactions = Transaction.objects.all()

    filters = {}

    filter_by_type = query_params.get('type')
    if filter_by_type:
        filters['type'] = filter_by_type

    filter_by_description = query_params.get('description')
    if filter_by_description:
        filters['description__icontains'] = filter_by_description

    if filters:
        transactions = transactions.filter(**filters)

    return transactions


@api_view(['POST', 'GET'])
def transaction_list_create(request):
    if request.method == 'POST':
        return create_new_transaction(request.data)

    if request.method == 'GET':
        filtered_transactions = get_filtered_transactions(request.query_params)
        paginator = StandardResultsSetPagination()

        page_transactions = paginator.paginate_queryset(filtered_transactions, request)

        serializer = TransactionSerializer(page_transactions, many=True)

        return paginator.get_paginated_response(serializer.data)

    return Response(status.HTTP_400_BAD_REQUEST)


def create_summary():
    summary = Transaction.objects.aggregate(
        total_income = Sum(
            'amount', filter=Q(type=TypeTransaction.INCOME)
        ),
        total_expense = Sum(
            'amount', filter=Q(type=TypeTransaction.EXPENSE)
        )
    )

    total_income = summary.get('total_income') or 0.00
    total_expense = summary.get('total_expense') or 0.00

    net_balance = total_income - total_expense

    return {
        'total_income': total_income,
        'total_expense': total_expense,
        'net_balance': net_balance
    }

@api_view(['GET'])
def summary_view(request):
    summary_data = create_summary()

    serializer = SummarySerializer(summary_data)

    return Response(serializer.data, status=status.HTTP_200_OK)