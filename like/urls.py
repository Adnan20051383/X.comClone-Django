from django.urls import path

from like import views

urlpatterns = [
    path('like-tweet/<str:tweet_id>', views.like_tweet, name='like_tweet'),
]
