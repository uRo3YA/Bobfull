from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import urls
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('list', UserViewSet) # 유저리스트 (테스트용)

urlpatterns =[
    # path('api-auth/', include('rest_framework.urls')),
    path("register/", views.RegisterAPIView.as_view()), # post - 회원가입
    path("auth/", views.AuthAPIView.as_view()), # post - 로그인, delete - 로그아웃, get - 유저정보
    path("auth/refresh/", TokenRefreshView.as_view()), # jwt 토큰 재발급
    path("", include(router.urls)),
]
