from django.shortcuts import render
from rest_framework import generics, mixins, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from restaurant.permissions import IsOwnerOrReadOnly
from rest_framework.pagination import LimitOffsetPagination

# Create your views here.
from .models import Restaurant, RestaurantLike
from .serializers import LikeSerializer, RestaurantSerializer

class RestaurantPagination(LimitOffsetPagination):
    default_limit = 10

class RestaurantViewSet(ModelViewSet):
   queryset = Restaurant.objects.all()
   permission_classes = [permissions.IsAdminUser]
   serializer_class = RestaurantSerializer
   pagination_class = RestaurantPagination
   filter_backends = [SearchFilter, DjangoFilterBackend]
   filterset_fields = ['category']
   search_fields = ['name', 'detail']

class Likelist(APIView):
    def get(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        likes = RestaurantLike.objects.filter(restaurant=restaurant)
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        # request.data는 사용자의 입력 데이터
        serializer = LikeSerializer(data=request.data)
        restaurant = Restaurant.objects.get(pk=pk)
        like = RestaurantLike.objects.filter(restaurant_id=pk, user=request.user)
        if serializer.is_valid():  # 유효성 검사
            if not like:
                serializer.validated_data["user"] = request.user
                serializer.validated_data["restaurant"] = restaurant
                serializer.save()  # 저장
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                like.delete()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)