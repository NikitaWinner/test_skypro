from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from typing import Optional, Union

from django.contrib.auth.models import User


class EmailBackend(ModelBackend):
    """
    Authenticate users by email using a custom backend.

    The EmailBackend class provides a custom backend for authenticating users by email.

    Methods:
        authenticate(self, request, username: Optional[str] = None, password: Optional[str] = None, **kwargs) -> Union[User, None]:
            Verify the entered email and password for correctness and return the user if authentication is successful.

    """

    def authenticate(self, request, username: Optional[str] = None, password: Optional[str] = None, **kwargs) -> Union[
        User, None]:
        """
        Authenticate a user by email and password.

        Attempt to authenticate a user based on the provided email and password.

        Args:
            request: The user's request object.
            username (str): The user's username (email).
            password (str): The user's password.
            **kwargs: Additional arguments (not used in this method).

        Returns:
            User: A user object if authentication is successful, or None otherwise.

        """
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password):
            return user
