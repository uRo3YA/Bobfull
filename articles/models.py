from django.db import models
from accounts.models import User
from django.conf import settings
from restaurant.models import Restaurant
# from multichat.models import ChatRoom
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
    id = models.AutoField(primary_key=True)
    #title = models.CharField(max_length=50)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    grade= models.CharField(max_length=10, choices=star_Choices)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    def __int__(self):
        return self.id

    # class Meta:
    #     db_table = '식당리뷰'

# # 이미지 업로드 경로
def image_upload_path(instance, filename):
    return f'review/{instance.review.id}/{filename}'

class Reviewimages(models.Model):
    id = models.AutoField(primary_key=True)
    review= models.ForeignKey(Review, on_delete=models.CASCADE, related_name='reviewimage')
    image = models.ImageField(null=True, blank=True,upload_to=image_upload_path)
    def __int__(self):
        return self.id

    # class Meta:
    #     db_table = '리뷰이미지'

class Matching_room(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    #from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    content = models.TextField()
    # members = models.ManyToManyField(settings.AUTH_USER_MODEL, symmetrical=False, related_name='members')
    member = models.ManyToManyField(User, symmetrical=False, related_name='members')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    chk_gender=models.BooleanField()
    chatroom=models.ForeignKey('multichat.ChatRoom',null=True, blank=True ,on_delete=models.SET_NULL,related_name='chatroom_id')
    # class Meta:
    #     db_table = '매칭룸'
## 같이 간 사람의 평가
class person_review(models.Model):
    ## 방 번호
    matching_room=models.ForeignKey(Matching_room,on_delete=models.CASCADE)
    ## 작성자
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    ## 평가요소
    evaluation=models.CharField(max_length=80,choices=eval_Choices)
    ## 평가할 멤버
    # to_member=models.ManyToManyField(Matching_room, related_name='review_members')
    # class Meta:
    #     db_table = '만남후기'