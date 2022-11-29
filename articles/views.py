from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from accounts.serializers import UserSerializer
from .serializers import ReviewSerializer,Matching_roomSerializer
from .models import Review,Matching_room
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.generics import get_object_or_404
# class ReviewList(APIView): # 목록 보여줌
#     def get(self, request): # 리스트 보여줄 때
#         reviews = Review.objects.all()
#         # 여러개 객체 serialize하려면 many=True
#         serializer = ReviewSerializer(reviews, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = ReviewSerializer(
#             data=request.data) # request.data는 사용자 입력 데이터
#         if serializer.is_valid():
#             serializer.save(user = self.request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ReviewDetail(APIView):
#     def get_object(self, pk): # Review 객체 가져오기
#         try:
#             return Review.objects.get(pk=pk)
#         except Review.DoesNotExist:
#             raise Http404
    
#     def get(self, request, pk, format=None): # Review detail 보기
#         review = self.get_object(pk)
#         serializer = ReviewSerializer(review)
#         return Response(serializer.data)
    
#     def put(self, request, pk, format=None): # Review 수정하기
#         review = self.get_object(pk)
#         serializer = ReviewSerializer(review, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk, format=None): # Review 삭제하기
#         review = self.get_object(pk)
#         review.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
       	# serializer.save() 재정의
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

class matching_roomViewSet(viewsets.ModelViewSet):
    queryset = Matching_room.objects.all()
    serializer_class = Matching_roomSerializer
       	# serializer.save() 재정의
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

# class MembertViewSet(viewsets.ModelViewSet):

#     queryset = Member.objects.all()
#     serializer_class = MemberSerializer
#     # print(serializer_class)
#     def perform_create(self, serializer):
#         serializer.save(user = self.request.user)
#         print(serializer)

    
    # Matching_room.objects.get(serializer.)
    # def perform_update(self, serializer):
    #     if  [] in  
class add_memberView(APIView): # 좋아요와 비슷한 로직. 토글 형식.
    def post(self, request,pk):
        # user가 2가지 있어서 혼동 방지를 위해 
        room = get_object_or_404(Matching_room, id=pk)
        me = request.user
        # print(you.followings.all())
        if me in room.member.all(): # users/models.py의 related_name=followers
            room.followings.remove(me) # (request.user)
            return Response("매칭을 취소했습니다.", status=status.HTTP_200_OK)
        else:
            room.member.add(me) # 너의 팔로워에 나를 더해라
            return Response("매칭을 참가했습니다.", status=status.HTTP_200_OK)

