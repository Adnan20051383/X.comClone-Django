from django.urls import path

from auth_user import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('sign-up/', views.signUp, name='sign-up'),
    path('sign-in/', auth_views.LoginView.as_view(template_name="sign-in.html",
                                                  redirect_authenticated_user=True), name='sign-in'),
    path('sign-out/', auth_views.LogoutView.as_view(template_name="sign-out.html"), name='sign-out'),
    path('profile/<str:username>', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
