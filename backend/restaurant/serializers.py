from rest_framework import serializers

from articles.models import Review
from .models import Restaurant, RestaurantImage, Category, RestaurantLike

class RestaurantImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    
    class Meta:
        model = RestaurantImage
        fields = ('image',)

class RestaurantSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    
    def get_images(self, obj):
        image = obj.restaurantimage.all()
        return RestaurantImageSerializer(instance=image, many=True, context=self.context).data
    
    def get_category_name(self, obj):
        return obj.category.name

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'address', 'category_name', 'images', 'detail')
        
    def create(self, validated_data):
        instance = Restaurant.objects.create(**validated_data)
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            RestaurantImage.objects.create(restaurant=instance, image=image_data)
        return instance

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.email")
    restaurant = serializers.ReadOnlyField(source="restaurant.pk")
    class Meta:
        model = RestaurantLike
        fields = '__all__'

class InfoRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        # model = RestaurantLike
        model = Restaurant
        fields = '__all__'

class InfoReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'