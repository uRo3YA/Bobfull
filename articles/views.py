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
from accounts.models import User
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        # print(context["request"])
        return context

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
    queryset = Matching_room.objects.all()
    serializer_class = Matching_roomSerializer
       	

    def perform_create(self, serializer):
        member=[self.request.user]
        store = get_object_or_404(Restaurant, id=self.kwargs['restaurant_id'])
        serializer.save(user=self.request.user,restaurant=store,member=member)
        
        # return super().perform_create(serializer)
    def get_queryset(self):
        qs = super().get_queryset()
        room = get_object_or_404(Restaurant, id=self.kwargs['restaurant_id'])
        qs = qs.filter(restaurant=self.kwargs['restaurant_id'])
       
        return qs

class add_memberView(APIView): # 좋아요와 비슷한 로직. 토글 형식.
    def post(self, request,restaurant_id,pk):
         
        room = get_object_or_404(Matching_room, id=pk)
        me = request.user
        if me in room.member.all(): #
            room.member.remove(me) # (request.user)
            return Response("매칭을 취소했습니다.", status=status.HTTP_200_OK)
        else:
            room.member.add(me) # 너의 룸에 나를 더해라
            return Response("매칭을 참가했습니다.", status=status.HTTP_200_OK)


class person_reviewViewSet(viewsets.ModelViewSet):
    
    queryset = person_review.objects.all()
    serializer_class = person_reviewSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
   
    def perform_create(self, serializer):
        room = get_object_or_404(Matching_room, id=self.kwargs['matching_room_id'])
        serializer.save(user = self.request.user, matching_room=room)
        review_data=(serializer.data)
        # print(review_data)
        # memdata=review_data['matching_room']['member']
        # print(memdata)
        #멤버 뽑아내기
        mem_data=review_data['matching_room']['member']

        for mem in mem_data:
            #작성자 멤버 삭제
            if mem==self.request.user.pk:
                continue
            else:
                user_info = get_object_or_404(User, pk=mem)
                if (review_data['evaluation']) =="매너가 좋았어요.":
                    manner_score=1
                    user_info.manner+=manner_score
                    user_info.save()
                elif (review_data['evaluation']) =="제 시간에 맞춰 왔어요.":
                    manner_score=0.5
                    user_info.manner+=manner_score
                    user_info.save()
                elif (review_data['evaluation']) =="여기는 뭐 추가?":
                    manner_score=-0.5
                    user_info.manner+=manner_score
                    user_info.save()
                elif (review_data['evaluation']) =="아이디어 없음":
                    manner_score=-1
                    user_info.manner+=manner_score
                    user_info.save()


    def perform_update(self, serializer):
        room = get_object_or_404(Matching_room, id=self.kwargs['matching_room_id'])
        serializer.save(user = self.request.user, matching_room=room)
        review_data=(serializer.data)
        # print(review_data)
        # #멤버 뽑아내기
        mem_data=review_data['matching_room']['member']   

        for mem in mem_data:
            #작성자 멤버 삭제
            if mem==self.request.user.pk:
                continue
            else:
                user_info = get_object_or_404(User, pk=mem)
                if (review_data['evaluation']) =="매너가 좋았어요.":
                    manner_score=1
                    user_info.manner+=manner_score
                    user_info.save()
                elif (review_data['evaluation']) =="제 시간에 맞춰 왔어요.":
                    manner_score=0.5
                    user_info.manner+=manner_score
                    user_info.save()
                elif (review_data['evaluation']) =="여기는 뭐 추가?":
                    manner_score=-0.5
                    user_info.manner+=manner_score
                    user_info.save()
                elif (review_data['evaluation']) =="아이디어 없음":
                    manner_score=-1
                    user_info.manner+=manner_score
                    user_info.save()
                # print(user_info)
                # print(user_info.manner)
        # print(review_data['evaluation'])

