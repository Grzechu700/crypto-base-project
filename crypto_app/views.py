from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
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
    transaction_type = request.GET.get("type")
    if transaction_type:
        transactions = transactions.filter(type=transaction_type)

    crypto_name = request.GET.get("crypto")
    if crypto_name:
        transactions = transactions.filter(
            Q(cryptocurrency__name__icontains=crypto_name) |
            Q(cryptocurrency__symbol__icontains=crypto_name)
        )
    return render(request,
                  "crypto_app/transactions.html",
                  {"transactions": transactions})


def portfolio(request):
    portfolio = Portfolio.objects.select_related("user", "cryptocurrency").all()

    for portfolio_item in portfolio:
        preferred_market_data = MarketData.objects.filter(
            cryptocurrency=portfolio_item.cryptocurrency,
            currency=portfolio_item.user.currency
        ).order_by("-created_at").first()

        if preferred_market_data:
            portfolio_item.price = preferred_market_data.price
            portfolio_item.currency = preferred_market_data.currency
        else:
            usd_market_data = MarketData.objects.filter(
                cryptocurrency=portfolio_item.cryptocurrency,
                currency="USD"
            ).order_by("-created_at").first()

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


@login_required
def dashboard(request):
    dashboard = {}

    for transaction in Transaction.objects.filter(user=request.user).order_by("-created_at")[:5].select_related("cryptocurrency"):
        symbol = transaction.cryptocurrency.symbol
        dashboard.setdefault(symbol, 0)
        if transaction.type == "BUY":
            dashboard[transaction.cryptocurrency.symbol] -= transaction.total_value
        else:
            dashboard[transaction.cryptocurrency.symbol] += transaction.total_value

    return render(request, "crypto_app/dashboard.html", {"dashboard": dashboard})


@login_required
def reports(request):
    user_transactions = Transaction.objects.filter(user=request.user).select_related("cryptocurrency")
    buy_count = 0
    sell_count = 0
    total_spent = 0
    total_earned = 0

    for transaction in user_transactions:
        if transaction.type == "BUY":
            buy_count += 1
            total_spent += transaction.total_value
        elif transaction.type == "SELL":
            sell_count += 1
            total_earned += transaction.total_value

    profit_loss = total_earned - total_spent

    context = {
        "buy_count": buy_count,
        "sell_count": sell_count,
        "total_spent": total_spent,
        "total_earned": total_earned,
        "profit_loss": profit_loss,
    }

    return render(request, "crypto_app/reports.html", context)
