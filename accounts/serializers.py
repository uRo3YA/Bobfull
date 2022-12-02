from rest_framework import serializers
from dj_rest_auth.serializers import UserDetailsSerializer
from .models import *

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class UserSerializer(UserDetailsSerializer):

    profile = ProfileSerializer()

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('profile',)

    def update(self, instance, validated_data):
        profile_serializer = self.fields['profile']
        profile_instance = instance.userprofile
        profile_data = validated_data.pop('profile', {})

        # to access the 'company_name' field in here
        alcohol = profile_data.get('alcohol')
        talk = profile_data.get('talk')
        smoke = profile_data.get('smoke')
        speed = profile_data.get('speed')
        gender = profile_data.get('gender')

        # update the userprofile fields
        profile_serializer.update(profile_instance, profile_data)

        instance = super().update(instance, validated_data)
        return instance
