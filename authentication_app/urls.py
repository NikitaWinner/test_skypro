from django.urls import path
from typing import Type, List, Path

from authentication_app import views
from authentication_app.apps import AuthenticationAppConfig

app_name = AuthenticationAppConfig.name

urlpatterns: List[Type[Path]] = [
    # Home View
    path("", views.HomeView.as_view(), name="home"),

    # Custom Login View
    path("login/", views.CustomLoginView.as_view(), name="login"),

    # Custom Logout View
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),

    # Register View
    path("register/", views.RegisterView.as_view(), name="register"),

    # Profile Edit View
    path("profile_edit/<int:pk>/", views.ProfileEditView.as_view(), name="profile_edit"),
]
