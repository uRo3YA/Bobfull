from rest_framework import serializers
from .models import Review,Matching_room,person_review
from accounts.models import User

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.nickname')
    class Meta:
        model = Review
        fields = ('id', 'title', 'content', 'updated_at','user','grade')



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
    user = serializers.ReadOnlyField(source = 'user.email')
    class Meta:
        model = person_review
        fields=('id', 'matching_room','user','evaluation' )
