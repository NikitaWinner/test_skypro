from rest_framework import status
from rest_framework.exceptions import APIException


class DuplicateUsername(APIException):
    """
    Исключение для обработки дублирования имени пользователя (username).

    Класс `DuplicateUsername` используется для генерации исключения, если в процессе регистрации
    нового пользователя обнаружено, что имя пользователя (username) уже существует в системе.

    Attributes:
        status_code (int): HTTP-код статуса ответа (400 Bad Request).
        default_detail (str): Сообщение по умолчанию для клиента (Username already exists.).
        default_code (str): Код ошибки по умолчанию (duplicate_username).

    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Username already exists.'
    default_code = 'duplicate_username'
