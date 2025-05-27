# gold_silver/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('gold_prices/', views.gold_prices, name='gold_prices'),
    path('silver_prices', views.silver_prices, name='silver_prices'),
]
