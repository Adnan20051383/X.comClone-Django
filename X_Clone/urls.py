"""
URL configuration for X_Clone project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from auth_user import views

urlpatterns = [
    path('', RedirectView.as_view(url='/users/sign-in/', permanent=True)),
    path('admin/', admin.site.urls),
    path('users/', include('auth_user.urls')),
    path('follows/', include('follow.urls')),
    path('home/', views.home, name='home'),
    path('notifications/', include('notif.urls')),
    path('tweets/', include('tweet.urls')),
    path('likes/', include('like.urls')),
    path('msg/', include('msg.urls'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
