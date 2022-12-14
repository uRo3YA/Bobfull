from django.shortcuts import render, redirect, get_object_or_404
from .models import ChatRoom, Message, UnreadMessage
from django.contrib.auth.decorators import login_required
from .forms import MessageForm
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import time
from rest_framework.response import Response
from rest_framework import status
from articles.models import Matching_room
from rest_framework.decorators import api_view
from .serializers import ChatRoomSerializer, MessageSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView



@api_view(['GET'])
def index(request):
    user = get_user_model().objects.get(pk=request.user.pk)
    # 유저가 속해있는 모든 채팅방
    rooms = user.user_chatroom.order_by("-updated_at")
    serializer = ChatRoomSerializer(rooms, many=True)
    new_data = []
    for s in serializer.data:
        room_pk = dict(s)['id']
        room = ChatRoom.objects.get(pk=room_pk)
        message = Message.objects.filter(room=room).order_by('created_at')
        # 유저가 각 채팅방별로 읽지 않은 메세지의 개수
        message_count = 0
        for m in message:
            if UnreadMessage.objects.get(message=m, user=user).read == False:
                message_count += 1
        data = {'message_count': message_count}
        data.update(s)
        new_data.append(data)
    return Response(new_data)


@api_view(['GET'])
def detail(request, room_pk):
    print(request.user.pk)
    room = get_object_or_404(ChatRoom, pk=room_pk)
    user = get_user_model().objects.get(pk=request.user.pk)
    messages = Message.objects.filter(room=room).order_by('created_at')
    serializer = MessageSerializer(messages, many=True)
    if request.user in room.users.all():
        # 메세지는 오래된 것부터 위에서부터 읽으니까...?
        # messages = Message.objects.filter(room=room).order_by('created_at')
        for m in messages:
            # 채팅창에 접속했으니까
            u = UnreadMessage.objects.get(message=m, user=user)
            # 안읽었던 것을 모두 읽음 처리 해준다
            if u.read == False:
                u.read = True
                u.save()   
        for m in messages:
            read = UnreadMessage.objects.filter(message=m, read=True).count()
            # 메세지를 읽지 않은 사람의 수
            unread = room.users.all().count() - read
            m.unread = unread
            m.save()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create(request, matchingroom_pk):
    host = get_user_model().objects.get(pk=request.user.pk)
    # users에는 matchingroom의 member가 와야함, create함수에 matchingroom pk를 받고 matchingroom의 member.all을 user로 설정 
    matching_room = Matching_room.objects.get(pk=matchingroom_pk)
    users = matching_room.member.all()
    room = ChatRoom.objects.create(host=host, matching_room=matching_room)
    room.save()
    # users를 room의 users에 하나하나씩 add해야함
    for u in users:
        room.users.add(u)
        room.save()
    serializer = ChatRoomSerializer(room)
    return Response(serializer.data)


# 매칭룸에는 있으나 채팅에는 없는 유저가 채팅창에 들어오려고함, 멤버로 add하고 채팅창에 들어가기까지 구현함
@api_view(['GET'])
def join(request, matchingroom_pk):
    user = get_user_model().objects.get(pk=request.user.pk)
    matching_room = Matching_room.objects.get(pk=matchingroom_pk)
    room = ChatRoom.objects.get(matching_room=matching_room)
    if user in matching_room.member.all() and user not in room.users.all():
        room.users.add(user)
        room.save()
        # 메세지는 오래된 것부터 위에서부터 읽으니까...?
        messages = Message.objects.filter(room=room).order_by('created_at')
        for m in messages:
            # 채팅창에 접속했으니까 기존에 채팅창에 있던 메세지들을 다 볼 수 있으니 True상태의 unreadmessage데이터를 생성함
            UnreadMessage.objects.create(message=m, user=user, read=True)  
        message_info = [] 
        for m in messages:
            read = UnreadMessage.objects.filter(message=m, read=True).count()
            # 메세지를 읽지 않은 사람의 수
            unread = room.users.all().count() - read
            m.unread = unread
            m.save()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    return Response({}, status=status.HTTP_400_BAD_REQUEST)

# 채팅방 떠나기
@api_view(["GET"])
def leave(request, room_pk):
    user = get_user_model().objects.get(pk=request.user.pk)
    room = get_object_or_404(ChatRoom, pk=room_pk)
    if user in room.users.all():
        room.users.remove(user)
        messages = Message.objects.filter(room=room)
        for m in messages:
            u = UnreadMessage.objects.get(message=m, user=user)
            u.delete()
        return Response({}, status=201)
    
@api_view(["DELETE"])
def finish(request, room_pk):
    room = get_object_or_404(ChatRoom, pk=room_pk)
    if room.host == get_user_model().objects.get(pk=request.user.pk):
        room.delete()
        return Response({}, status=201)

#    
# @csrf_exempt   
# @api_view(["GET", "POST"])
# def send(request, room_pk):
#     room = ChatRoom.objects.get(pk=room_pk)
#     if request.method == "GET":
#         messages = Message.objects.filter(room=room).order_by('-created_at')
#         serializer = MessageSerializer(messages, many=True)
#         return Response(serializer.data)
#     elif request.method == "POST":
#         # data = JSONParser().parse(request)
#         serializer = MessageSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             sender = get_user_model().objects.get(pk=request.user.pk)
#             room.last_user = sender
#             room.last_message = serializer.content
#             room.save()
#             serializer.save(room=room, sender=sender)
#             for member in room.users.all():
#                 # 모든 user에 대해 메세지 안읽음 데이터 만들고
#                 UnreadMessage.objects.create(message=serializer, user=member)
#             # 메세지 보낸 사람만 메세지 읽음 처리
#             u = UnreadMessage.objects.get(message=serializer, user=serializer.sender)
#             u.read = True
#             u.save()
#             unread = UnreadMessage.objects.filter(message=serializer, read=False)
#             serializer.save(unread=unread)
#             return Response(serializer.data, status=201)
#     return Response(serializer.errors, status=400)

class Send(APIView):
    def get(self, request, room_pk):
        room = ChatRoom.objects.get(pk=room_pk)
        messages = Message.objects.filter(room=room).order_by('-created_at')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    def post(self, request, room_pk):
        room = ChatRoom.objects.get(pk=room_pk)
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            sender = get_user_model().objects.get(pk=request.user.pk)
            room.last_user = sender
            room.last_message = serializer.validated_data['content']
            room.save()
            message = serializer.save(sender_id=request.user.pk, room_id=room_pk)
            for member in room.users.all():
                # 모든 user에 대해 메세지 안읽음 데이터 만들고
                UnreadMessage.objects.create(message=message, user=member)
            # 메세지 보낸 사람만 메세지 읽음 처리
            u = UnreadMessage.objects.get(message=message, user=sender)
            u.read = True
            u.save()
            unread = UnreadMessage.objects.filter(message=message, read=False).count()
            serializer.save(unread=unread)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
