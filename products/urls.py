from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),  # ✅ Add this line
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('<int:product_id>/toggle-save/', views.toggle_save_product, name='toggle_save_product'),
]
