from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils import timezone

from msg.models import Msg, MsgSession
from notif.models import Notification


# Create your views here.

@login_required
def show_chat(request, receiver):
    user = User.objects.get(id=receiver)
    condition = Q(sender=request.user, receiver=user) | Q(receiver=request.user, sender=user)
    messages_sent = Msg.objects.filter(condition).order_by('created_at')
    Msg.objects.filter(receiver=request.user, sender=user).update(is_seen=True)
    notifications = Notification.objects.filter(user=request.user, is_seen=False).count()
    context = {
        'messages_sent': messages_sent,
        'receiver': user,
        'notifications': notifications,
    }
    return render(request, 'chat-msg.html', context)


def create_message(request, receiver):
    user = User.objects.get(id=receiver)
    text = request.POST['text-msg']
    img = None
    if 'img-msg' in request.FILES:
        img = request.FILES['img-msg']
    if not (img or text):
        return redirect(show_chat, receiver)
    else:
        msg = Msg(sender=request.user, receiver=user, text=text, image=img)
        msg.save()
        condition = Q(user1=request.user, user2=user) | Q(user2=request.user, user1=user)
        MsgSession.objects.filter(condition).update(updated_at=timezone.now())
        return redirect(show_chat, receiver)


def show_msg_sessions(request):
    condition = Q(user1=request.user) | Q(user2=request.user)
    msg_sessions = MsgSession.objects.filter(condition).order_by('-updated_at')
    notifications = Notification.objects.filter(user=request.user, is_seen=False).count()
    sender_users = []
    for msg_session in msg_sessions:
        if msg_session.user1 != request.user:
            sender_users.append(msg_session.user1)
        if msg_session.user2 != request.user:
            sender_users.append(msg_session.user2)

    new_messages_num = []
    for sender in sender_users:
        new_messages_num.append(Msg.objects.filter(sender=sender, receiver=request.user, is_seen=False).count())
    zipped = zip(msg_sessions, sender_users, new_messages_num)
    context = {
        'zipped': zipped,
        'notifications': notifications,
    }
    return render(request, 'msg-sessions.html', context)
