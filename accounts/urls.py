from django.urls import path
from .views import home_view, CustomPasswordChangeView 
from . import views 
from items import views as item_views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.urls import path, include

app_name = 'accounts'


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('home/', home_view, name='home'),
    path('mypage/', views.mypage_view, name='mypage'), 
    path('', views.home_view, name='home'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),  
    path('email/change/', views.email_change_view, name='email_change'),
    
    path('logout/', views.logout_view, name='logout'),
   
    path('password/change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('user-posts/', include('items.urls')),
   

]
