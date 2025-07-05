"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from accounts.views import home_view 
from django.conf import settings
from django.conf.urls.static import static
from portfolio import views as portfolio_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', portfolio_views.portfolio_top, name='portfolio_top'),  # ←ポートフォリオ用トップページ
    path('accounts/', include('accounts.urls')),
    path('items/', include('items.urls')),
    path('home/', home_view, name='home'),
    
    path('oshimate/', include('items.urls')),
    #path('', lambda request: redirect('accounts:login')),

    
   
]

# ↓ urlpatterns の定義「の後」に追記すること！
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)