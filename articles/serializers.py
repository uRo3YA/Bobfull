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



class Matching_roomSerializer(serializers.ModelSerializer):
    # member = UserSerializer(many=True)
    restaurant = serializers.ReadOnlyField(source = 'restaurant.name')
    class Meta:
        model = Matching_room
        fields = ('id','title', 'from_date','to_date','content','member','restaurant')

class person_reviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.email')
    class Meta:
        model = person_review
        fields=('id', 'matching_room','user','evaluation' )
