from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from notif import views

urlpatterns = [
    path('', views.show_notif, name='notifications'),
    path('<str:notif_id>/', views.delete_notif, name='delete-notif'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)