from django.db import models
from accounts.models import User
from django.conf import settings
star_Choices = (
    ("⭐", "⭐"),
    ("⭐⭐", "⭐⭐"),
    ("⭐⭐⭐", "⭐⭐⭐"),
    ("⭐⭐⭐⭐", "⭐⭐⭐⭐"),
    ("⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"),
)
eval_Choices=(
    ("매너가 좋았어요.","매너가 좋았어요."),
    ("제 시간에 맞춰 왔어요.","제 시간에 맞춰 왔어요."),
    ("여기는 뭐 추가?","여기는 뭐 추가?"),
    ("아이디어 없음","아이디어 없음"),
)



## 식당 후기를 작성
class Review(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    grade= models.CharField(max_length=10, choices=star_Choices)
    ## 필요한 것들
    # 레스토랑 정보
    # 같이 간 사람 수?
    # 댓글도 필요한가?
# class Matching_room(models.Model):
#     title = models.CharField(max_length=50)
#     from_date = models.DateTimeField()
#     to_date = models.DateTimeField()
#     content = models.TextField()
#     users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name= 'member')

class Matching_room(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    content = models.TextField()
    # members = models.ManyToManyField(settings.AUTH_USER_MODEL, symmetrical=False, related_name='members')
    member = models.ManyToManyField(User, symmetrical=False, related_name='members')

## 같이 간 사람의 평가
class person_review(models.Model):
    ## 방 번호
    matching_room=models.ForeignKey(Matching_room,on_delete=models.CASCADE)
    ## 작성자
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    ## 평가요소
    evaluation=models.TextField(choices=eval_Choices)
    ## 