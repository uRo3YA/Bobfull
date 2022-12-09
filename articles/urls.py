from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
# from .views import *
from .views import ReviewViewSet,matching_roomViewSet,person_reviewViewSet
from . import views
# review 목록 보여주기
review_list = ReviewViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

# review detail 보여주기 + 수정 + 삭제
review_detail = ReviewViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})
# matching_room 목록 보여주기
matching_room_list = matching_roomViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

# matching_room 보여주기 + 수정 + 삭제
matching_room_detail = matching_roomViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

# matching_room 목록 보여주기
matching_room_review_list = person_reviewViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

# matching_room 보여주기 + 수정 + 삭제
matching_room_review_detail = person_reviewViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})


urlpatterns = [
    # path('review/', ReviewList.as_view()),
    # path('review/<int:pk>/', ReviewDetail.as_view()),
    path('<int:restaurant_id>/review/', review_list),
    path('<int:restaurant_id>/review/<int:pk>/', review_detail),
    path('<int:restaurant_id>/matching_room/', matching_room_list),
    path('<int:restaurant_id>/matching_room/<int:pk>/', matching_room_detail),
    # path('member/', member_list),
    # path('member/<int:pk>/', member_detail),
    # path('member/<int:pk>/add/', views.PostLikeAPIView.as_view(), name='post_like'),
    path('<int:restaurant_id>/matching_room/<int:pk>/add/', views.add_memberView.as_view(), name="add_member"), # 멤버추가
    # path('matching_room/<int:pk>/review/add/',views.person_reviewView.as_view(), name="add_personreview")# 사람 후기
    path('<int:restaurant_id>/matching_room/<int:matching_room_id>/review/',matching_room_review_list),
    path('<int:restaurant_id>/matching_room/<int:matching_room_id>/review/<int:pk>/',matching_room_review_detail)
    ]

urlpatterns = format_suffix_patterns(urlpatterns)