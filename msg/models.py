from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.db.models import ImageField
from django.db.models.signals import post_save
from django.utils import timezone

from notif.models import Notification


class Msg(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    text = models.TextField(null=True, blank=True)
    image = ImageField(upload_to='msg_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def add_msg(sender, instance, *args, **kwargs):
        msg = instance
        sender_user = msg.sender
        user = msg.receiver
        notification_type = 4
        notif = Notification(sender=sender_user, user=user, notification_type=notification_type)
        notif.save()
        if not (MsgSession.objects.filter(user1=user, user2=sender_user).exists() or MsgSession.objects.filter(user2=user, user1=sender_user).exists()):
            msg_session = MsgSession(user1=user, user2=sender_user)
            msg_session.save()

    def time_difference_from_now(self):
        now = timezone.now()  # This ensures now is timezone-aware
        diff = now - self.created_at

        if diff < timedelta(minutes=1):
            return f"{int(diff.seconds)} seconds ago"
        elif diff < timedelta(hours=1):
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        elif diff < timedelta(days=1):
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff < timedelta(days=30):
            days = diff.days
            return f"{days} day{'s' if days > 1 else ''} ago"
        elif diff < timedelta(days=365):
            months = diff.days // 30
            return f"{months} month{'s' if months > 1 else ''} ago"
        else:
            years = diff.days // 365
            return f"{years} year{'s' if years > 1 else ''} ago"


class MsgSession(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


post_save.connect(Msg.add_msg, sender=Msg)
