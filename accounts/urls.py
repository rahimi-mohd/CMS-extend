from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "accounts"
urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="accounts/logout.html"),
        name="logout",
    ),
    path("register_user/", views.register_user, name="register_user"),
    path("user_profile/<int:pk>/", views.user_profile, name="user_profile"),
    path("user_list/", views.user_list, name="user_list"),
    path(
        "user_profile/<int:pk>/edit_profile/",
        views.update_user_profile,
        name="edit_profile",
    ),
]
