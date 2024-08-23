from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from tweet import views

urlpatterns = [
    path('create-tweet/', views.create_tweet, name='create-tweet'),
    path('tweet-detail/<str:tweet_id>/', views.show_tweet, name='tweet-detail'),
    path('reply/<str:parent_id>/', views.replyTweet, name='reply-tweet'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
