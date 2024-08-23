from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from auth_user.forms import SignUpForm, EditProfileForm
from auth_user.models import Profile
from follow.models import Follow
from like.models import Like
from notif.models import Notification
from tweet.models import Tweet, Stream


def signUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('sign-up')
        else:
            return render(request, 'sign-up.html', {'form': form})
    elif request.user.is_authenticated:
        return redirect('profile', username=request.user.username)
    else:
        form = SignUpForm()
        context = {
            'form': form,
        }
        return render(request, 'sign-up.html', context)


@login_required
def profile_view(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    followers = Follow.objects.filter(following=user).count()
    followings = Follow.objects.filter(follower=user).count()
    fallow_status = Follow.objects.filter(follower=request.user, following=user)
    notifications = Notification.objects.filter(user=request.user, is_seen=False)
    user_tweets = Tweet.objects.filter(user=user, parent_id=None)
    bio = profile.bio
    image = profile.image
    context = {
        'profile': profile,
        'followers': followers,
        'followings': followings,
        'bio': bio,
        'image': image,
        'user': user,
        'follow_status': fallow_status,
        'authenticated_user': request.user,
        'notifications': notifications.count(),
        'user_tweets': user_tweets,
    }
    return render(request, 'profile.html', context)


@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    initial_data = {'first_name': profile.first_name,
                    'last_name': profile.last_name,
                    'bio': profile.bio,
                    'address': profile.address,
                    'phone_number': profile.phone,
                    'image': profile.image}
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, initial=initial_data)
        if form.is_valid():
            profile.image = form.cleaned_data.get('image')
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.bio = form.cleaned_data.get('bio')
            profile.address = form.cleaned_data.get('address')
            profile.phone = form.cleaned_data.get('phone_number')
            profile.save()
            return redirect('profile', username=request.user.username)
        else:
            context = {
                'form': form,
                'profile': profile,
            }
            return render(request, 'edit-profile.html', context)
    else:
        form = EditProfileForm(initial=initial_data)
        context = {
            'form': form,
            'profile': profile,
        }
        return render(request, 'edit-profile.html', context)


@login_required
def home(request):
    notifications = Notification.objects.filter(user=request.user, is_seen=False)
    streams = Stream.objects.filter(follower=request.user).order_by('-created_at')
    message = list(messages.get_messages(request))
    liked_tweets = []
    for like in Like.objects.filter(liker=request.user):
        liked_tweets.append(like.tweet.id)
    context = {
        'authenticated_user': request.user,
        'notifications': notifications.count(),
        'streams': streams,
        'message': message,
        'liked_tweets': liked_tweets,
    }
    return render(request, 'home.html', context)