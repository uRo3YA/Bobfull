from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from .serializers import ReviewSerializer,Matching_roomSerializer,person_reviewSerializer
from .models import Review,Matching_room,person_review
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.generics import get_object_or_404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.db.models import Q

from restaurant.models import Restaurant


class ReviewViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


    def perform_create(self, serializer):
        store = get_object_or_404(Restaurant, id=self.kwargs['restaurant_id'])
        serializer.save(user=self.request.user,restaurant=store)
        
        return super().perform_create(serializer)
    def get_queryset(self):
        qs = super().get_queryset()
        room = get_object_or_404(Restaurant, id=self.kwargs['restaurant_id'])
        qs = qs.filter(restaurant=self.kwargs['restaurant_id'])
       
        return qs
        # return super().perform_create(serializer)

class matching_roomViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    queryset = Matching_room.objects.all()
    serializer_class = Matching_roomSerializer
       	

    def perform_create(self, serializer):
        
        serializer.save(user=self.request.user)
        
        # return super().perform_create(serializer)


class add_memberView(APIView): # 좋아요와 비슷한 로직. 토글 형식.
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    def post(self, request,pk):
         
        room = get_object_or_404(Matching_room, id=pk)
        me = request.user
        if me in room.member.all(): #
            room.member.remove(me) # (request.user)
            return Response("매칭을 취소했습니다.", status=status.HTTP_200_OK)
        else:
            room.member.add(me) # 너의 룸에 나를 더해라
            return Response("매칭을 참가했습니다.", status=status.HTTP_200_OK)

class person_reviewViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    queryset = person_review.objects.all()
    serializer_class = person_reviewSerializer

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(matching_room=self.kwargs['pk'])
        
        return qs