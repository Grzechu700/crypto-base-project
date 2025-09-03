from django.contrib import admin
from .models import User, Cryptocurrency, MarketData, Transaction, Portfolio


admin.site.register(User)
admin.site.register(Cryptocurrency)
admin.site.register(MarketData)
admin.site.register(Transaction)
admin.site.register(Portfolio)
