from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_delete

from notif.models import Notification


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower_set")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_set")
    created_at = models.DateTimeField(auto_now_add=True)

    def user_following(sender, instance, *args, **kwargs):
        follow = instance
        sender_user = follow.follower
        user = follow.following
        notif = Notification(sender=sender_user, user=user, notification_type=1)
        notif.save()

    def user_unfollowing(sender, instance, *args, **kwargs):
        follow = instance
        sender_user = follow.follower
        user = follow.following
        if Notification.objects.filter(sender=sender_user, notification_type=1, user=user).exists():
            notif = Notification.objects.get(sender=sender_user, notification_type=1, user=user)
            notif.delete()


post_save.connect(Follow.user_following, sender=Follow)
post_delete.connect(Follow.user_unfollowing, sender=Follow)
