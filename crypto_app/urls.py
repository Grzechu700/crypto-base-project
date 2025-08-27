from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name='index'),
    path("cryptocurrencies/", views.cryptocurrencies, name="cryptocurrencies"),
    path("transactions/", views.transactions, name="transactions"),
    path("portfolio/", views.portfolio, name="portfolio"),

]