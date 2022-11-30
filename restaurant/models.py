from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class Category(models.Model):
    category_choices = (
        ('족발·보쌈', '족발·보쌈'),
        ('찜·탕·찌개', '찜·탕·찌개'),
        ('일식', '일식'),
        ('피자', '피자'),
        ('고기', '고기'),
        ('야식', '야식'),
        ('양식', '양식'),
        ('치킨', '치킨'),
        ('중식', '중식'),
        ('아시안', '아시안'),
        ('백반·죽·국수', '백반·죽·국수'),
        ('분식', '분식'),
        ('카페·디저트', '카페·디저트'),
        ('패스트푸드', '패스트푸드'),
    )
    name = models.CharField(max_length=20, choices=category_choices)
    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='category')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_restaurants', blank=True)

def user_directory_path(instance, filename):
    return f'images/{instance.restaurant.id}/{filename}'

class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='restaurantimage')
    image = models.ImageField(upload_to=user_directory_path)
    

    