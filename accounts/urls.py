from .views import home_view

# accounts/urls.py の先頭に追記
app_name = 'accounts'


from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('home/', home_view, name='home')

]
