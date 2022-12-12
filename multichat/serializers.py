from rest_framework import serializers

from articles.models import Matching_room
from .models import ChatRoom, Message, UnreadMessage

class ChatRoomSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ChatRoom
        fields = '__all__'
        depth = 2
        
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        depth = 2 
        
