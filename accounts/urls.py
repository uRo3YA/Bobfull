from django.urls import path, include
from .views import ProfileAPI
from .views import *

profile_detail = ProfileAPI.as_view({
    'get': 'retrieve',
})

urlpatterns =[
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('<int:pk>/profile/', profile_detail, name='profile-detail'),
]
