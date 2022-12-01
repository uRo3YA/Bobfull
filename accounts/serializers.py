from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerialize

class CustomRegisterSerializer(RegisterSerializer):
    # 기본 설정 필드: username, password, email
    # 추가 설정 필드: alcohol, talk, smoke, speed, gender, manner
    alcohol = serializers.BooleanField()    
    talk = serializers.BooleanField()    
    smoke = serializers.BooleanField()    
    speed = serializers.IntegerField()   
    gender = serializers.BooleanField() # False가 남자    
    manner = serializers.FloatField(default=36.5)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['alcohol'] = self.validated_data.get('alcohol', '')
        data['talk'] = self.validated_data.get('talk', '')
        data['smoke'] = self.validated_data.get('smoke', '')
        data['speed'] = self.validated_data.get('speed', '')
        data['gender'] = self.validated_data.get('gender', '')
        data['manner'] = self.validated_data.get('manner', '')
        return data

