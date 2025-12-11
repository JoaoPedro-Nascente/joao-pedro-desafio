from rest_framework import serializers
from decimal import Decimal

from ..models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    def validate_amount(self, value):
        if value <= Decimal('0.00'):
            raise serializers.ValidationError("'Amount' must be positive and greater than zero.")
        
        return value
    
    class Meta:
        model = Transaction
        fields = "__all__"

class SummarySerializer(serializers.Serializer):
    total_income = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_expense = serializers.DecimalField(max_digits=15, decimal_places=2)
    net_balance = serializers.DecimalField(max_digits=15, decimal_places=2)