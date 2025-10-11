# blog/urls.py

from django.urls import path
from . import views

app_name = 'blog'  # ✅ this is required when using namespace

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('<int:pk>/', views.blog_detail, name='blog_detail'),
]
