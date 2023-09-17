from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    """
    Аутентификация пользователя по email с использованием кастомного бэкенда.

    Класс EmailBackend предоставляет кастомный бэкенд для аутентификации
    пользователей по email.

    Methods:
        authenticate(self, request, username=None, password=None, **kwargs):
            Проверяет введенный email и пароль пользователя на корректность и
            возвращает пользователя, если аутентификация успешна.

    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Аутентификация пользователя по email и паролю.

        Попытка аутентификации пользователя по предоставленному email и паролю.

        Args:
            request: Объект запроса пользователя.
            username (str): Имя пользователя (email).
            password (str): Пароль пользователя.
            **kwargs: Дополнительные аргументы (не используются в данном методе).

        Returns:
            User: Объект пользователя, если аутентификация успешна, в противном случае None.

        """
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password):
            return user
