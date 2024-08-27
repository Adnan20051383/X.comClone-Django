from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from msg import views

urlpatterns = [
    path('show-chat/<int:receiver>/', views.show_chat, name='show-chat'),
    path('create-msg/<int:receiver>/', views.create_message, name='create-msg'),
    path('msg-session/', views.show_msg_sessions, name='msg-session'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)