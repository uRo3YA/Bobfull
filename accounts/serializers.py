from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer

from .models import User
from dj_rest_auth.serializers import UserDetailsSerializer

class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            "nickname",
            "alcohol",
            "talk",
            "smoke",
            "speed",
            "gender",
        )

class CustomUserRegisterSerializer(RegisterSerializer):
    # 기본 설정 필드: nickname, password, email
    # 추가 설정 필드: alcohol, talk, smoke, speed, gender, manner
    nickname = serializers.CharField()
    def get_cleaned_data(self):
        super(CustomUserRegisterSerializer, self).get_cleaned_data()
        return {
            "email": self.validated_data.get("email", ""),
            "nickname": self.validated_data.get("nickname", ""),
            "password1": self.validated_data.get("password1", ""),
            "password2": self.validated_data.get("password2", ""),
        }

    def save(self, request):
        user = super().save(request)
        user.nickname = self.data.get("nickname")
        user.save()
        return user
