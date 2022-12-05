from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

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

class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='category_restaurants')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_restaurants', blank=True)
    detail = models.TextField()

def user_directory_path(instance, filename):
    return f'images/{instance.restaurant.id}/{filename}'

class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='restaurantimage')
    image = models.ImageField(upload_to=user_directory_path)
    

    