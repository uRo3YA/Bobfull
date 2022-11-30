from rest_framework import serializers
from .models import Review,Matching_room,person_review
from accounts.serializers import UserSerializer
from accounts.models import User




class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.nickname')
    class Meta:
        model = Review
        fields = ('id', 'title', 'content', 'updated_at','user','grade')

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
    class Meta:
        model = person_review
        fields=('id', 'matching_room','user','evaluation')
# class MemberSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source = 'user.nickname')
#     class Meta:
#         model = Member
#         fields = ['id', 'matching_room', 'user']

# class PostLikeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Matching_room
#         fields = ['members']