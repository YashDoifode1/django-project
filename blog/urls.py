from django.urls import path
from . import views

app_name = 'blog'  # ✅ important if you include it in project urls.py

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('<int:pk>/', views.blog_detail, name='blog_detail'),  # ✅ this name must exist
]
