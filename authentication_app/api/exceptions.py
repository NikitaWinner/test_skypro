from rest_framework import status
from rest_framework.exceptions import APIException


class DuplicateUsername(APIException):
    """
    Exception for handling duplicate usernames.

    The `DuplicateUsername` class is used to raise an exception when attempting to register
    a new user with a username that already exists in the system.

    Attributes:
        status_code (int): The HTTP response status code (400 Bad Request).
        default_detail (str): The default message for the client ("Username already exists.").
        default_code (str): The default error code ("duplicate_username").

    Raises:
        DuplicateUsername: An exception indicating that the username already exists.

    Examples:
        To raise this exception, you can use it in your view like this::

            if username_exists:
                raise DuplicateUsername()
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Username already exists.'
    default_code = 'duplicate_username'
