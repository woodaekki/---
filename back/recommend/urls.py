# recommend/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('recommend/', views.recommend_products, name='recommend_products'),
]
