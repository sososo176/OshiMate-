from django.urls import path
from .views import home_view
from . import views
# accounts/urls.py の先頭に追記
app_name = 'accounts'


from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('home/', home_view, name='home'),
    path('mypage/', views.mypage_view, name='mypage'), 
    path('', views.home_view, name='home'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),  # ← これを追加！
    path('email/change/', views.email_change_view, name='email_change'),
    path('password/change/', views.password_change_view, name='password_change'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),




]
