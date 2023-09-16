from django.contrib.auth import authenticate
from rest_framework import serializers
from authentication_app.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели CustomUser.
    """

    class Meta:
        model = CustomUser
        # Поля, которые будут включены в сериализацию
        fields = ('id', 'email', 'password', 'is_staff', 'is_active', 'date_joined')
        # Поля, которые будут только для чтения (не могут быть изменены через API)
        read_only_fields = ('id', 'is_staff', 'is_active', 'date_joined')


class AuthTokenSerializer(serializers.Serializer):
    """
    Сериализатор для аутентификации (логина) пользователя.
    """

    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'},
                                     trim_whitespace=False)

    def validate(self, attrs):
        """
        Валидация email и пароля пользователя.

        Проверяет введенный email и пароль пользователя на корректность.
        Если аутентификация успешна, возвращает атрибут 'user' с пользователем.

        Args:
            attrs (dict): Словарь атрибутов, включая email и password.

        Returns:
            dict: Словарь атрибутов с пользователем, если аутентификация успешна.

        Raises:
            serializers.ValidationError: Если аутентификация не удалась или email и/или пароль не предоставлены.
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
