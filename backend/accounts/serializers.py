from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from restaurant.serializers import InfoRestaurantSerializer, InfoReviewSerializer

from .models import User
from dj_rest_auth.serializers import UserDetailsSerializer

from restaurant.models import RestaurantLike ,Restaurant
from articles.models import Review

class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            "nickname",
            "alcohol",
            "talk",
            "smoke",
            "speed",
            "gender",
            "manner",
            "profile_image",
        )
        read_only_fields = ('manner', )

class CustomUserRegisterSerializer(RegisterSerializer):
    # 기본 설정 필드: nickname, password, email
    # 추가 설정 필드: alcohol, talk, smoke, speed, gender, manner, profile_image
    def get_cleaned_data(self):
        super(CustomUserRegisterSerializer, self).get_cleaned_data()
        return {
            "email": self.validated_data.get("email", ""),
            "password1": self.validated_data.get("password1", ""),
            "password2": self.validated_data.get("password2", ""),
        }

    def save(self, request):
        user = super().save(request)
        user.save()
        return user

class UserInfo(serializers.ModelSerializer):
    user = CustomUserDetailsSerializer(read_only=True)
    restaurants = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    def get_restaurants(self, user):
        like_data=(RestaurantLike.objects.filter(user=user))
        restaurants = list(Restaurant.objects.filter(id__in=like_data))
        # restaurants = list(RestaurantLike.objects.filter(user=user))
        return InfoRestaurantSerializer(restaurants, many=True).data
        

    def get_reviews(self, user):
        reviews = list(Review.objects.filter(user=user))
        # print(reviews)
        return InfoReviewSerializer(reviews, many=True).data
    # def get_restaurants(self, obj):
    #     restaurants = list(obj.restaurant_set.all())
    #     return InfoRestaurantSerializer(restaurants, many=True).data

    # def get_reviews(self, obj):
    #     reviews = list(obj.review_set.all())
    #     return InfoReviewSerializer(reviews, many=True).data
    class Meta:
        model = User
        fields = '__all__'