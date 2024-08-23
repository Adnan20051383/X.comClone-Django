from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from like.models import Like
from notif.models import Notification
from tweet.models import Tweet


def create_tweet(request):
    caption = request.POST['caption']
    if 'image' in request.FILES:
        image = request.FILES['image']
    else:
        image = None
    if caption or image:
        tweet = Tweet(tweet=caption, image=image, user=request.user)
        tweet.save()
    else:
        message = messages.add_message(request, messages.ERROR, 'No caption or image. The Tweet Is Not Created!')
        previous_url = request.META.get('HTTP_REFERER', '/sss/')
        return redirect(previous_url)
    return redirect('home')


@login_required
def show_tweet(request, tweet_id):
    tweet = Tweet.objects.get(id=tweet_id)
    notifications = Notification.objects.filter(user=request.user, is_seen=False)
    parent_tweet = None
    if tweet.parent_id:
        parent_tweet = Tweet.objects.get(id=tweet.parent_id)
    authenticated_user = request.user
    like_status = Like.objects.filter(liker=authenticated_user, tweet=tweet).exists()
    comments = Tweet.objects.filter(parent_id=tweet_id).order_by('-created_at')
    liked_comments = Like.objects.filter(liker=authenticated_user)
    liked_comments_ids = []
    for liked_comment in liked_comments:
        liked_comments_ids.append(liked_comment.tweet.id)
    message = list(messages.get_messages(request))
    context = {'tweet': tweet, 'authenticated_user': authenticated_user, 'like_status': like_status, 'comments': comments, 'message': message,
               'liked_comments_ids': liked_comments_ids, 'parent_tweet': parent_tweet, 'notifications': notifications.count()}
    return render(request, 'post-detail.html', context)


@login_required
def replyTweet(request, parent_id):
    parent_tweet = Tweet.objects.get(id=parent_id)
    text = request.POST['comment-text']
    image = None
    if 'comment-image' in request.FILES:
        image = request.FILES['comment-image']

    if not (text or image):
        message = messages.add_message(request, messages.ERROR, 'No caption or image. The Comment Is Not Created!')
        previous_url = request.META.get('HTTP_REFERER', '/sss/')
        return redirect(previous_url)
    else:
        new_tweet = Tweet(tweet=text, user=request.user, parent_id=parent_id, image=image)
        new_tweet.save()
        Tweet.objects.filter(id=parent_id).update(comments=Tweet.objects.filter(parent_id=parent_id).count())
        previous_url = request.META.get('HTTP_REFERER', '/sss/')
        return redirect(previous_url)
