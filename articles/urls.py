from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
# from .views import *
from .views import ReviewViewSet

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

urlpatterns = [
    # path('review/', ReviewList.as_view()),
    # path('review/<int:pk>/', ReviewDetail.as_view()),
    path('review/', review_list),
    path('review/<int:pk>/', review_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)