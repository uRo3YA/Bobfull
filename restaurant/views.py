from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.http import Http404
from django.shortcuts import get_object_or_404

# Create your views here.
from .models import Restaurant
from .serializers import RestaurantSerializer

class RestaurantViewSet(ModelViewSet):
   queryset = Restaurant.objects.all()
   serializer_class = RestaurantSerializer
   


