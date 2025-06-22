# items/urls.py
from django.urls import path
from .views import item_create_view
from . import views

app_name = 'items'

urlpatterns = [
    path('create/', item_create_view, name='create'),
    path('<int:pk>/', views.item_detail_view, name='item_detail'),
]
