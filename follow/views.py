from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from follow.models import Follow


def follow(request, following):
    if request.method == 'POST':
        followed = User.objects.get(username=following)
        follow_status = Follow.objects.filter(follower=request.user, following=followed).exists()
        if follow_status:
            follow = Follow.objects.filter(follower=request.user, following=followed)
            follow.delete()
        else:
            follow = Follow(follower=request.user, following=followed)
            follow.save()
        previous_url = request.META.get('HTTP_REFERER', '/sss/')
        return redirect(previous_url)

@login_required
def show_followers(request, username):
    user = User.objects.get(username=username)
    followers_follow = Follow.objects.filter(following=user)
    followers = []
    for follower in followers_follow:
        followers.append(follower.follower)
    followers_count = Follow.objects.filter(following=user).count()
    context = {'followers': followers, 'follow_count': followers_count, 'title': 'Followers'}
    return render(request, 'followers-followings-list.html', context)


def show_followings(request, username):
    user = User.objects.get(username=username)
    followings_follow = Follow.objects.filter(follower=user)
    followings = []
    for following in followings_follow:
        followings.append(following.following)
    followings_count = Follow.objects.filter(follower=user).count()
    context = {'followers': followings, 'follow_count': followings_count, 'title': 'Followings'}
    return render(request, 'followers-followings-list.html', context)

