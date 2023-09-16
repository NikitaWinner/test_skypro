from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from .serializers import CustomUserSerializer, AuthTokenSerializer


class CustomUserRegistration(generics.CreateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.instance
        user.set_password(request.data['password'])
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        headers = self.get_success_headers(serializer.data)

        return Response(
            {"token": token.key, "user": CustomUserSerializer(user).data},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': CustomUserSerializer(user).data})
