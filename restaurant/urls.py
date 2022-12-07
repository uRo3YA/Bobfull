from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet
from . import views

router = DefaultRouter()
router.register('', RestaurantViewSet)
urlpatterns = [
   path('', include(router.urls)),
   path('<int:pk>/like/', views.Likelist.as_view()),
]