from django.urls import path
from .views import home_view
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
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),  # ← これを追加！
    path('email/change/', views.email_change_view, name='email_change'),
    path('password/change/', views.password_change_view, name='password_change'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('password/change/', auth_views.PasswordChangeView.as_view(
    template_name='accounts/password_change.html',
    success_url=reverse_lazy('accounts:password_change_done')
), name='password_change'),
    path('password/change/done/', auth_views.PasswordChangeDoneView.as_view(
    template_name='accounts/password_change_done.html'
), name='password_change_done'),
    path('user-posts/', include('items.urls')),  
    

]
