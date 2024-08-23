from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE
from django.utils import timezone

from tweet.models import Tweet


class Notification(models.Model):
    NOTIFICATION_CHOICES = ((1, 'follow'), (2, 'like'), (3, 'comment'))

    tweet = models.ForeignKey(Tweet, null=True, blank=True, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=CASCADE, related_name='sender_notif')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_notif')
    notification_type = models.IntegerField(choices=NOTIFICATION_CHOICES, blank=True)
    notif_msg = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

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
