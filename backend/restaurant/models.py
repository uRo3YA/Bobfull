from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from accounts.models import User

class Category(models.Model):
    category_choices = (
        ('한식', '한식'),
        ('일식', '일식'),
        ('중식', '중식'),
        ('양식', '양식'),
        ('분식', '분식'),
        ('피자', '피자'),
        ('치킨', '치킨'),
        ('고기', '고기'),
        ('아시안', '아시안'),
        ('술집', '술집'),
        ('카페·디저트', '카페·디저트'),
        ('패스트푸드', '패스트푸드'),
        ('기타', '기타'),
    )
    name = models.CharField(max_length=20, choices=category_choices)
    def __str__(self):
        return self.name
    # class Meta:
    #     db_table = '식당 카테고리'

class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='category_restaurants')
    detail = models.TextField()
    # class Meta:
    #     db_table = '식당 정보'

def user_directory_path(instance, filename):
    return f'images/{instance.restaurant.id}/{filename}'

class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='restaurantimage')
    image = models.ImageField(upload_to=user_directory_path)
    # class Meta:
    #     db_table = '식당 이미지'

# 음식점 좋아요(북마크)
class RestaurantLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    # class Meta:
    #     db_table = '식당 북마크'

    
    

    