from rest_framework import serializers
from .models import Review,Matching_room,person_review,Reviewimages
from accounts.models import User

class ReviewImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    
    class Meta:
        model = Reviewimages
        fields = ('image',)

class ReviewSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source = 'user.id')
    
    def get_images(self, obj):
        image = obj.reviewimage.all()
        return ReviewImageSerializer(instance=image, many=True).data

    class Meta:
        model = Review
        # fields = ('id', 'title', 'content', 'updated_at','user','grade','images',)
        fields = ('id','content', 'updated_at','user','grade','images',)
        # fields = '__all__'

    def create(self, validated_data):
        instance = Review.objects.create(**validated_data)
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            Reviewimages.objects.create(review=instance, image=image_data)
        return instance

class Matching_roomSerializer(serializers.ModelSerializer):
    member = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all())
    user = serializers.ReadOnlyField(source = 'user.id')
    # member = serializers.ReadOnlyField(source = 'user.email')
    restaurant = serializers.ReadOnlyField(source = 'restaurant.name')
    class Meta:
        model = Matching_room
        fields = ('id','user','title', 'from_date','to_date','content','member','restaurant')

class person_reviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = person_review
        fields=('id', 'matching_room','user','evaluation' )
# class MemberSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source = 'user.nickname')
#     class Meta:
#         model = Member
#         fields = ['id', 'matching_room', 'user']

# class PostLikeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Matching_room
#         fields = ['members']