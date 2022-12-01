from rest_framework import serializers
from .models import Restaurant, RestaurantImage

class RestaurantImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    
    class Meta:
        model = RestaurantImage
        fields = ('image',)

class RestaurantSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    
    def get_images(self, obj):
        image = obj.restaurantimage.all()
        return RestaurantImageSerializer(instance=image, many=True, context=self.context).data

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'address', 'category', 'images',)
        
    def create(self, validated_data):
        instance = Restaurant.objects.create(**validated_data)
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            RestaurantImage.objects.create(restaurant=instance, image=image_data)
        return instance

