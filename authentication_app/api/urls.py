from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.CustomUserRegistration.as_view(), name='register'),  # https://<domain>/api/v1/register/
    path('login/', views.CustomObtainAuthToken.as_view(), name='login'),  # https://<domain>/api/v1/login/
]
