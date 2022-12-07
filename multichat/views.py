from django.shortcuts import render, redirect, get_object_or_404
from .models import ChatRoom, Message, UnreadMessage
from django.contrib.auth.decorators import login_required
from .forms import MessageForm
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import time


@login_required
def index(request):
    user = get_user_model().objects.get(pk=request.user.pk)
    # 유저가 속해있는 모든 채팅방
    rooms = user.user_chatroom.filter(finished=False).order_by("-updated_at")
    rooms_info = []
    for r in rooms:
        message = Message.objects.filter(room=r).order_by('created_at')
        # 유저가 각 채팅방별로 읽지 않은 메세지의 개수
        m_count = 0
        for m in message:
            if UnreadMessage.objects.get(message=m, user=user).read == False:
                m_count += 1
        rooms_info.append((r.host, r.users.all, r.last_user, r.last_message, m_count, r.pk))
    context = {"rooms": rooms_info}
    return render(request, "multichat/index.html", context)


@login_required
def detail(request, room_pk):
    room = get_object_or_404(ChatRoom, pk=room_pk)
    user = get_user_model().objects.get(pk=request.user.pk)
    # user가 속한 모든 room, detail페이지에는 굳이 없어도 될 듯?
    rooms = user.user_chatroom.all()
    if request.user in room.users.all():
        # 메세지는 오래된 것부터 위에서부터 읽으니까...?
        messages = Message.objects.filter(room=room).order_by('created_at')
        for m in messages:
            # 채팅창에 접속했으니까
            u = UnreadMessage.objects.get(message=m, user=user)
            # 안읽었던 것을 모두 읽음 처리 해준다
            if u.read == False:
                u.read = True
                u.save()   
        message_info = [] 
        for m in messages:
            read = UnreadMessage.objects.filter(message=m, read=True).count()
            # 메세지를 읽지 않은 사람의 수
            unread = room.users.all().count() - read
            message_info.append((m.sender, m.content, m.created_at, unread))
        form = MessageForm()
        context = {
            "room": room,
            "rooms": rooms.order_by("-updated_at"),
            "message_info": message_info,
            "form": form,
        }
        return render(request, "multichat/detail.html", context)
    return redirect("multichat:index")

@login_required
def create(request):
    host = get_user_model().objects.get(pk=request.user.pk)
    # users에는 matchingroom의 member가 와야함, create함수에 matchingroom pk를 받고 matchingroom의 member.all을 user로 설정
    # 이건 임시방편으로 모든 유저로 채팅 만든겨 
    users = get_user_model().objects.all()
    room = ChatRoom.objects.create(host=host)
    room.save()
    # users를 room의 users에 하나하나씩 add해야함
    for u in users:
        room.users.add(u)
        room.save()
    context = {'room': room}
    return redirect("multichat:index")

# 일단은 끝난 채팅창을 안보임 처리만 해두고 db삭제 구현은 못했음 return밑으로 안돌아가더라
@login_required
def finish(request, room_pk):
    room = get_object_or_404(ChatRoom, pk=room_pk)
    if room.host == get_user_model().objects.get(pk=request.user.pk):
        room.finished = True
        room.save()
        return redirect("multichat:index")
        time.sleep(60)
        room.delete()
        
        
@require_POST
def send(request, room_pk):
    form = MessageForm(request.POST)
    room = ChatRoom.objects.get(pk=room_pk)
    if form.is_valid():
        # content만 담긴 메세지 commit False처리
        message = form.save(commit=False)
        message.room = room
        message.sender = get_user_model().objects.get(pk=request.user.pk)
        message.save()
        room.last_user = message.sender
        room.last_message = message.content
        room.save()
        for member in room.users.all():
            # 모든 user에 대해 메세지 안읽음 데이터 만들고
            UnreadMessage.objects.create(message=message, user=member)
        # 메세지 보낸 사람만 메세지 읽음 처리
        u = UnreadMessage.objects.get(message=message, user=message.sender)
        u.read = True
        u.save()
        # messages = Message.objects.filter(room=room).order_by('-created_at')
        # context = {'messages': messages}
        # return JsonResponse(context)
        return redirect("multichat:detail", room_pk)  
    return render(request, "multichat/detail.html", {"form": form})