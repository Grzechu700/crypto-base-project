from django.shortcuts import render
from .models import Cryptocurrency, Transaction, Portfolio, MarketData


def index(request):
    return render(request, "crypto_app/index.html")

def cryptocurrencies(request):
    cryptocurrencies = Cryptocurrency.objects.all()
    return render(request,
                  "crypto_app/cryptocurrencies.html",
                  {"cryptocurrencies": cryptocurrencies})


def transactions(request):
    transactions = Transaction.objects.select_related("user", "cryptocurrency").all()

    return render(request,
                  "crypto_app/transactions.html",
                  {"transactions": transactions})


def portfolio(request):
    portfolio = Portfolio.objects.select_related("user", "cryptocurrency").all()

    for portfolio_item in portfolio:
        preferred_market_data = MarketData.objects.filter(
            cryptocurrency=portfolio_item.cryptocurrency,
            currency=portfolio_item.user.currency
        ).order_by("-date").first()

        if preferred_market_data:
            portfolio_item.price = preferred_market_data.price
            portfolio_item.currency = preferred_market_data.currency
        else:
            usd_market_data = MarketData.objects.filter(
                cryptocurrency=portfolio_item.cryptocurrency,
                currency="USD"
            ).order_by("-date").first()

            if usd_market_data:
                portfolio_item.price = usd_market_data.price
                portfolio_item.currency = "USD"
            else:
                portfolio_item.price = None
                portfolio_item.currency = "N/A"
                portfolio_item.total_value = None
                portfolio_item.has_price_data = False


        if portfolio_item.price is not None:
            portfolio_item.total_value = portfolio_item.amount * portfolio_item.price

    return render(request, "crypto_app/portfolio.html", {"portfolio": portfolio})
