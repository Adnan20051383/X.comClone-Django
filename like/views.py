from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from like.models import Like
from tweet.models import Tweet


def like_tweet(request, tweet_id):
    if Tweet.objects.filter(id=tweet_id).exists():
        tweet = Tweet.objects.get(id=tweet_id)
        if Like.objects.filter(tweet=tweet, liker=request.user).exists():
            like = Like.objects.get(tweet=tweet, liker=request.user)
            like.delete()
            Tweet.objects.filter(id=tweet_id).update(likes=Like.objects.filter(tweet=tweet).count())
        else:
            like = Like(tweet=tweet, liker=request.user)
            like.save()
            Tweet.objects.filter(id=tweet_id).update(likes=Like.objects.filter(tweet=tweet).count())

    previous_url = request.META.get('HTTP_REFERER', '/sss/')
    return redirect(previous_url)
