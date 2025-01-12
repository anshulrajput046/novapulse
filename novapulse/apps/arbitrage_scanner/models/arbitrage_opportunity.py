

from django.db import models
from django_extensions.db.models import TimeStampedModel


class ArbitrageOpportunity(TimeStampedModel):
    direction = models.CharField(max_length=20, null=True, blank=True)
    symbol = models.CharField(max_length=10)
    binance_price = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    solana_price = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    profit = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)

    def __str__(self):
        return f"{self.symbol} ({self.direction})"
