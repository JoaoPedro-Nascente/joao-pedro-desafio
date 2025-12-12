from rest_framework import serializers
from decimal import Decimal

from ..models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    
    class Meta:
        model = Transaction
        fields = "__all__"

        read_only_fields = ('user',)

class SummarySerializer(serializers.Serializer):
    total_income = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_expense = serializers.DecimalField(max_digits=15, decimal_places=2)
    net_balance = serializers.DecimalField(max_digits=15, decimal_places=2)