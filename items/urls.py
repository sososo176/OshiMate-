# items/urls.py
from django.urls import path
from .views import item_create_view

app_name = 'items'

urlpatterns = [
    path('create/', item_create_view, name='create'),
]
