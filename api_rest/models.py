from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
import uuid

class TypeTransaction(models.TextChoices):
    """
    Classe auxiliar de Transaction.transaction_type
    """
    INCOME = "income", "Income Transaction"
    OUTCOME = "outcome", "Outcome Transaction"

class Transaction(models.Model):
    """
    Modelo principal
    """
    transaction_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    transaction_description = models.CharField(
        max_length=100,
        default=""
    )

    transaction_amount = models.DecimalField(
        default=0.0,
        max_digits=12,
        decimal_places=2,
        validators=[
            MinValueValidator(0.0)
        ]
    )
    
    transaction_type = models.CharField(
        max_length=50,
        choices=TypeTransaction.choices
    )
    
    transaction_date = models.DateField(
        default=timezone.now
    )

    def __str__(self):
        return super().__str__()