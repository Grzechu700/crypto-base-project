from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    CURRENCY_CHOICES = [
        ("USD", "USD"),
        ("PLN", "PLN"),
        ("EUR", "Euro"),
        ("GBP", "British Pound")
    ]

    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="PLN")

    def __str__(self):
        return self.username


class Cryptocurrency(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.symbol})"


class MarketData(models.Model):
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=8)
    volume = models.DecimalField(max_digits=20, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    CURRENCY_CHOICES = [
        ("USD", "USD"),
        ("PLN", "PLN"),
        ("EUR", "Euro"),
        ("GBP", "British Pound")
    ]

    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="PLN")

    def __str__(self):
        return f"{self.cryptocurrency.symbol} - {self.currency} - {self.price}"


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=[("Purchase", "BUY"), ("Sale", "SELL")])
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.amount} - {self.cryptocurrency.symbol}"


class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=8)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.cryptocurrency.symbol}"

    class Meta:
        unique_together = ("user", "cryptocurrency")

