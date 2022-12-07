"""bobfull URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from accounts.views import UserViewSet

# 유저 전체 정보 확인
# http://127.0.0.1:8000/user/로 접속
router = routers.DefaultRouter()
router.register('user', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls')),
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/', include('accounts.urls')),
    # path('accounts/', include('dj_rest_auth.registration.urls')),
    path('restaurant/', include('restaurant.urls')),
    path('', include(router.urls)),
    path('multichat/', include('multichat.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
