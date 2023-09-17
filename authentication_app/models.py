from django.contrib.auth.models import PermissionsMixin, BaseUserManager, AbstractBaseUser
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Менеджер пользователей для модели CustomUser.

    UserManager - это пользовательский менеджер, который предоставляет методы для
    создания и управления пользователями.

    Methods:
        create_user(self, email: str, password: str = None, **extra_fields) -> CustomUser: Создает и сохраняет пользователя с заданными параметрами.
        create_superuser(self, email: str, password: str = None, **extra_fields) -> CustomUser: Создает и сохраняет суперпользователя с заданными параметрами.

    """

    def create_user(self, email: str, password: str = None, **extra_fields) -> 'CustomUser':
        """
        Создает и сохраняет пользователя с заданными параметрами.

        Args:
            email (str): Email пользователя.
            password (str): Пароль пользователя.
            **extra_fields (dict): Дополнительные поля пользователя.

        Returns:
            CustomUser: Созданный пользователь.

        Raises:
            ValueError: Если не указан email.

        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str = None, **extra_fields) -> 'CustomUser':
        """
        Создает и сохраняет суперпользователя с заданными параметрами.

        Args:
            email (str): Email суперпользователя.
            password (str): Пароль суперпользователя.
            **extra_fields (dict): Дополнительные поля суперпользователя.

        Returns:
            CustomUser: Созданный суперпользователь.

        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Пользовательская модель пользователя.

    Модель CustomUser представляет собой пользовательскую модель, которая
    наследует AbstractBaseUser и PermissionsMixin. Она используется для создания
    пользователей с уникальным email вместо стандартного username.

    Attributes:
        email (str): Email пользователя.
        is_staff (bool): Показывает, является ли пользователь сотрудником.
        is_active (bool): Показывает, активен ли пользователь.
        date_joined (datetime): Дата и время регистрации пользователя.

    Methods:
        email_user(self, subject: str, message: str, from_email: str = None, **kwargs): Отправляет email пользователю.

    """

    email = models.EmailField(
        _("email address"),
        max_length=256,
        unique=True,
        error_messages={
            "unique": _("A user with that email address already exists."),
        },
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. \
            Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject: str, message: str, from_email: str = None, **kwargs):
        """
        Отправляет email пользователю.

        Args:
            subject (str): Заголовок сообщения.
            message (str): Текст сообщения.
            from_email (str, optional): Email отправителя.
            **kwargs: Дополнительные аргументы для send_mail.

        """
        send_mail(subject, message, from_email, [self.email], **kwargs)
