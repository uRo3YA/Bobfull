from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.
from .models import Restaurant
from .serializers import RestaurantSerializer

class RestaurantViewSet(ModelViewSet):
   authentication_classes = [JWTAuthentication]
   queryset = Restaurant.objects.all()
   serializer_class = RestaurantSerializer
   
   filter_backends = [SearchFilter, DjangoFilterBackend]
   filterset_fields = ['category']
   search_fields = ['name', 'detail']
   
   
   


