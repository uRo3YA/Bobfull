from rest_framework import serializers

from multichat.serializers import ChatRoomSerializer
from .models import Review,Matching_room,person_review,Reviewimages
from accounts.models import User
from accounts.serializers import CustomUserDetailsSerializer
class ReviewImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    
    class Meta:
        model = Reviewimages
        fields = ('image',)

class ReviewSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source = 'user.nickname')
    
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
    user = CustomUserDetailsSerializer(read_only=True)
    nickname = serializers.ReadOnlyField(source = 'user.nickname')
    # member = serializers.ReadOnlyField(source = 'user.email')
    restaurant_id = serializers.ReadOnlyField(source = 'restaurant.id')
    restaurant_name = serializers.ReadOnlyField(source = 'restaurant.name')
    chatroom= ChatRoomSerializer(read_only=True)
    class Meta:
        model = Matching_room
        fields = ('id','user','title','to_date','content','member','restaurant_id','restaurant_name', 'nickname','chk_gender','chatroom')
        # fields ='__all__'

class person_reviewSerializer(serializers.ModelSerializer):
    # to_member=serializers.SerializerMethodField()
    # matching_room=serializers.ReadOnlyField(source = 'person_review.matching_room')
    matching_room = Matching_roomSerializer(read_only=True)
    # print(matching_room)
    # def get_to_member(self,matching_room):
    #     # print(matching_room.id)
    #     room = (Matching_room.objects.get(pk=int(matching_room.id)))
        
    #     a=(room.member).all()
    #     mem=[]
    #     for i in a:
    #         mem.append(i.id)
   
    #     return mem
    class Meta:
        model = person_review
        fields='__all__'
        # fields=('id','matching_room','user','evaluation',) 
