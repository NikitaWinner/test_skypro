from typing import Tuple

from django.db.models import Model
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from django.contrib.auth import get_user_model


class EmailOrUsernameTokenAuthentication(TokenAuthentication):
    """
    Аутентификация пользователя по токену с учетом email или username.

    Класс EmailOrUsernameTokenAuthentication расширяет стандартный TokenAuthentication
    для аутентификации пользователя по токену. Он позволяет аутентифицировать пользователя
    как по email, так и по username.

    Attributes:
        model (Model): Модель пользователя, используемая в проекте.

    Methods:
        authenticate_credentials(self, key: str) -> Tuple[Model, None]: Проверяет корректность токена и возвращает пользователя,
        если аутентификация успешна.

    Raises:
        exceptions.AuthenticationFailed: Если токен неверен, пользователь не существует
        или учетная запись пользователя неактивна.

    """

    def authenticate_credentials(self, key: str) -> Tuple[Model, None]:
        model = get_user_model()
        try:
            user, _ = self.get_model().objects.get_or_create(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
        if not user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')
        return (user, None)
