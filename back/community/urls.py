from django.urls import path
from . import views

# community/urls.py

urlpatterns = [
    path('articles/', views.article_list),
    path('articles/<int:article_pk>/', views.article_detail),
    path('articles/<int:community_pk>/reviews/',  views.create_review),
    path('articles/<int:community_pk>/reviews/<int:review_pk>/', views.delete_review),
    path('fixed_articles/', views.fixed_article_list),
    path('fixed_articles/<int:pk>/', views.fixed_article_detail),

]
