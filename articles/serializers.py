from rest_framework import serializers
from .models import Review,Matching_room,person_review

from accounts.models import User
from restaurant.models import Restaurant
from restaurant.serializers import RestaurantSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.email')
    restaurant = serializers.ReadOnlyField(source = 'restaurant.name')
    class Meta:
        model = Review
        fields = ('id', 'title', 'content', 'updated_at','user','restaurant','grade')

# class Matching_roomSerializer(serializers.ModelSerializer):
#     persons = UserSerializer(many=True)
#     def create(self, validated_data):
#         persons = validated_data.pop('persons')
#         matching_room = Matching_room.objects.create(**validated_data)
#         if persons: # Bombs without this check
#             User.objects.create(matching_room=matching_room, **persons)  # Errors here
#         return matching_room
#     class Meta:
#         model = Matching_room

class Matching_roomSerializer(serializers.ModelSerializer):
    # member = UserSerializer(many=True)

    class Meta:
        model = Matching_room
        fields = ('id','title', 'from_date','to_date','content','member')

class person_reviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.email')
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