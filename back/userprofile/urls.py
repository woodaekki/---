# userprofile/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.create_profile, name='create_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/my_profile/', views.my_profile, name='my_profile'),
    path('profile/like-deposit/<str:product_id>/', views.like_deposit, name='like_deposit'),
    path('profile/like-saving/<str:product_id>/', views.like_saving, name='like_saving'),

]
