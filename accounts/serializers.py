from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['nickname', 'email', 'name', 'password','alcohol','talk','smoke','speed','gender']
        fields = '__all__'
        
    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            nickname = validated_data['nickname'],
            name = validated_data['name'],
            password = validated_data['password'],
            alcohol = validated_data['alcohol'],
            talk = validated_data['talk'],
            smoke = validated_data['smoke'],
            speed = validated_data['speed'],
            gender = validated_data['gender'],
        )
        return user
    