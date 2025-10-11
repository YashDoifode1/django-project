# products/urls.py

from django.urls import path
from . import views

app_name = 'products'  # ✅ add this line

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
]
