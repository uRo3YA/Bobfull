from django.db import models
from django.db import models
from django.conf import settings
from articles.models import Matching_room

# Create your models here.

class ChatRoom(models.Model):
    # create함수에서
    # host는 request.user로 일단 넣고
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='host_chatroom')
    # 얘는 matchingroom의 member
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_chatroom')
    matching_room = models.ForeignKey(Matching_room, on_delete=models.CASCADE)
    # send함수로 넣을 수 있음, create에서는 일단은 없는게 당연함
    last_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    last_message = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    # finish함수를 통해서 구현하고, finish된 후 하루 정도 지나면 자동으로 delete되게 -> 필요없을듯...
    # finished = models.BooleanField(default=False)
    # finished_at = models.DateTimeField(auto_now=True)
    # class Meta:
    #     db_table = '채팅룸'
class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    # request.user == sender
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    unread = models.IntegerField(default=0)

    # class Meta:
    #     db_table = '채팅메세지'


# 유저별로 모든 메세지에 대해 read TF를 만들어놓고 읽으면 T로 바꾸는 작업, message의 room_number로 거르고
# 채팅방 안읽은사람 count하고, room_number마다 안읽은 메세지 count하고
class UnreadMessage(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    # class Meta:
    #     db_table = '안읽은 메세지'

