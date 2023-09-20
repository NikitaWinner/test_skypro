from typing import Tuple

from django.db.models import Model
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from django.contrib.auth import get_user_model


class EmailOrUsernameTokenAuthentication(TokenAuthentication):
    """
    Authenticate a user via a token while considering email or username.

    The EmailOrUsernameTokenAuthentication class extends the standard TokenAuthentication
    to authenticate a user via a token. It allows authentication using either the email
    or username.

    Attributes:
        model (Model): The user model used in the project.

    Methods:
        authenticate_credentials(self, key: str) -> Tuple[Model, None]:
        Authenticate a user's credentials using the provided token key.

    Raises:
        exceptions.AuthenticationFailed: If the token is invalid, the user does not exist,
        or the user account is inactive.

    """

    def authenticate_credentials(self, key: str) -> Tuple[Model, None]:
        """
        Authenticate a user's credentials using the provided token key.

        Args:
            key (str): The token key for authentication.

        Returns:
            Tuple[Model, None]: A tuple containing the authenticated user and None.

        Raises:
            exceptions.AuthenticationFailed: If the token is invalid, the user does not exist,
            or the user account is inactive.
        """
        model = get_user_model()
        try:
            user, _ = self.get_model().objects.get_or_create(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
        if not user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')
        return (user, None)
