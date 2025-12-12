from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid

class TypeTransaction(models.TextChoices):
    """
    Classe auxiliar de Transaction.transaction_type
    """
    INCOME = "income", "Income Transaction"
    EXPENSE = "expense", "Expense Transaction"

class Transaction(models.Model):
    """
    Modelo principal
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    description = models.CharField(
        max_length=100,
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal(0.01))
        ]
    )
    
    type = models.CharField(
        max_length=50,
        choices=TypeTransaction.choices,
    )
    
    date = models.DateField(
    )

    def __str__(self):
        return f"{self.description}, {self.date}, valor: R${self.amount}, tipo: {self.type}"