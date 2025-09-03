import statistics
from enum import StrEnum
from django.db import models
from django.contrib.auth.models import AbstractUser


class Currency(StrEnum):
    USD = "USD"
    PLN = "PLN"
    EUR = "EUR"
    GBP = "GBP"


CURRENCY_CHOICES = [
    (Currency.USD, "US Dollar"),
    (Currency.PLN, "Polish Zloty"),
    (Currency.EUR, "Euro"),
    (Currency.GBP, "British Pound"),
]


class TransactionType(StrEnum):
    BUY = "BUY"
    SELL = "SELL"


TRANSACTION_TYPE_CHOICES = [
    (TransactionType.BUY, "Purchase"),
    (TransactionType.SELL, "Sale")
]


class User(AbstractUser):
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="PLN")

    def __str__(self):
        return self.username


class Cryptocurrency(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.symbol})"

    @property
    def trading_recommendation(self):
        latest_data = MarketData.objects.filter(cryptocurrency=self).order_by("-created_at").first()
        if not latest_data:
            return "Out of data"

        last_price = latest_data.price

        last_7_days = MarketData.objects.filter(cryptocurrency=self).order_by("-created_at")[:7]
        if len(last_7_days) < 7:
            return "Out of data"

        average_price = statistics.mean([data.price for data in last_7_days])

        percent_change = (last_price - average_price) / average_price * 100

        if percent_change < -5:
            return "Buy"
        elif percent_change > 5:
            return "Sell"
        else:
            return "Hold"


class MarketData(models.Model):
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=8)
    volume = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="PLN")

    def __str__(self):
        return f"{self.cryptocurrency.symbol} - {self.currency} - {self.price}"


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.amount} - {self.cryptocurrency.symbol}"

    @property
    def total_value(self):
        return self.amount * self.price


class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=8)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.cryptocurrency.symbol}"

    class Meta:
        unique_together = ("user", "cryptocurrency")

