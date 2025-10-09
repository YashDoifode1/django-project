from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='products'),  # <-- this name is important
    path('<int:pk>/', views.product_detail, name='product_detail'),
]
