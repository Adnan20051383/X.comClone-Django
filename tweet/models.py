from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.utils import timezone

from django.apps import apps



class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_id = models.IntegerField(null=True)
    tweet = models.TextField()
    image = models.ImageField(upload_to='post_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    def add_comment(sender, instance, *argrs, **kwargs):
        comment = instance
        if comment.parent_id is not None:
            sender_user = comment.user
            tweets = []
            tweet = comment
            while tweet.parent_id is not None:
                tweet1 = Tweet.objects.get(id=tweet.parent_id)
                tweets.append(tweet1)
                tweet = tweet1
            notification_type = 3
            Notification = apps.get_model('notif', 'Notification')
            for tweet2 in tweets:
                notif = Notification(sender=sender_user, user=tweet2.user, tweet=comment,
                                     notification_type=notification_type)
                notif.save()

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


class Stream(models.Model):
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def add_tweet(sender, instance, *args, **kwargs):
        tweet = instance
        if tweet.parent_id is None:
            followed = tweet.user
            Follow = apps.get_model('follow', 'Follow')
            followers = Follow.objects.filter(following=followed)

            for follower in followers:
                stream = Stream(tweet=tweet, followed=followed, follower=follower.follower)
                stream.save()

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


post_save.connect(Stream.add_tweet, sender=Tweet)
post_save.connect(Tweet.add_comment, sender=Tweet)
