# finance/urls.py

from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'deposits', views.DepositProductsViewSet)
router.register(r'deposit-options', views.DepositOptionsViewSet)
router.register(r'savings', views.SavingProductsViewSet)
router.register(r'saving-options', views.SavingOptionsViewSet)


urlpatterns = [
    path('save-products/', views.save_products),
    path('deposit-products/', views.deposit_products),
    path('deposit-product-options/<str:fin_prdt_cd>/', views.deposit_product_options),
    path('saving-products/', views.saving_products),
    path('saving-product-options/<str:fin_prdt_cd>/', views.saving_product_options),
    path('load/', include(router.urls)),
    path('get-product-code/', views.get_product_code),
    path('deposit-options/', views.all_deposit_options, name='all-deposit-options'),
    path('saving-options/', views.all_saving_options, name='all-saving-options'),
]
