from django.contrib.auth import authenticate
from rest_framework import serializers
from authentication_app.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model.
    """

    class Meta:
        model = CustomUser

        fields = ('id', 'email', 'password', 'is_staff', 'is_active', 'date_joined')

        read_only_fields = ('id', 'is_staff', 'is_active', 'date_joined')


class AuthTokenSerializer(serializers.Serializer):
    """
    Serializer for authenticating (logging in) a user.
    """

    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'},
                                     trim_whitespace=False)

    def validate(self, attrs):
        """
        Validate the user's email and password.

        Checks the entered email and password for correctness.
        If authentication is successful, returns the 'user' attribute with the user.

        Args:
            attrs (dict): A dictionary of attributes including email and password.

        Returns:
            dict: A dictionary of attributes with the user if authentication is successful.

        Raises:
            serializers.ValidationError: If authentication fails or if email and/or password are not provided.
        """
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)

            if user:
                attrs['user'] = user
                return attrs
            else:
                raise serializers.ValidationError('Incorrect email or password.')
        else:
            raise serializers.ValidationError('Both email and password are required.')
