from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from follow import views


urlpatterns = [
    path('<str:following>/', views.follow, name='follow'),
    path('followers/<str:username>', views.show_followers, name='show-followers'),
    path('followings/<str:username>', views.show_followings, name='show-followings'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)