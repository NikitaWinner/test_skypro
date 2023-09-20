from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from .serializers import CustomUserSerializer, AuthTokenSerializer


class CustomUserRegistration(generics.CreateAPIView):
    """
    API view for user registration.

    This view allows users to register by providing their information.

    Attributes:
        serializer_class (Serializer): The serializer class to use for user registration.
        permission_classes (tuple): The permission classes applied to this view.

    Methods:
        post(request, *args, **kwargs): Handle POST requests for user registration.
    """
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for user registration.

        Args:
            request (Request): The HTTP request object.
            *args: Variable-length argument list.
            **kwargs: Keyword arguments.

        Returns:
            Response: A response containing a token and user data upon successful registration.
        """
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
    """
    Custom token-based authentication view.

    This view allows users to obtain authentication tokens by providing valid credentials.

    Methods:
        post(request, *args, **kwargs): Handle POST requests for token authentication.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for token authentication.

        Args:
            request (Request): The HTTP request object.
            *args: Variable-length argument list.
            **kwargs: Keyword arguments.

        Returns:
            Response: A response containing an authentication token upon successful authentication.
        """
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': CustomUserSerializer(user).data})
