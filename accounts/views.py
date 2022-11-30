from django.shortcuts import get_object_or_404
from rest_framework import response, viewsets
from .serializers import ProfileSerializer
from .models import User

class ProfileAPI(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        profile_serializer = ProfileSerializer(user.profile)
        return response(profile_serializer.data)