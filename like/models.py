from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.utils import timezone

from notif.models import Notification
from tweet.models import Tweet


class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def add_like(sender, instance, *args, **kwargs):
        like = instance
        sender_user = like.liker
        user = like.tweet.user
        notif = Notification(sender=sender_user, user=user, tweet=like.tweet, notification_type=2)
        notif.save()

    def delete_like(sender, instance, *args, **kwargs):
        like = instance
        sender_user = like.liker
        user = like.tweet.user
        if Notification.objects.filter(sender=sender_user, user=user, tweet=like.tweet, notification_type=2).exists():
            notif = Notification(sender=sender_user, user=user, tweet=like.tweet, notification_type=2)
            notif.delete()

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


post_save.connect(Like.add_like, sender=Like)
post_delete.connect(Like.delete_like, sender=Like)