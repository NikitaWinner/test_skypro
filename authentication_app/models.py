from django.contrib.auth.models import PermissionsMixin, BaseUserManager, AbstractBaseUser
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user manager for the CustomUser model.

    UserManager is a custom manager that provides methods for
    creating and managing users.

    Methods:
        create_user(self, email: str, password: str = None, **extra_fields) -> 'CustomUser':
            Creates and saves a user with the given parameters.
        create_superuser(self, email: str, password: str = None, **extra_fields) -> 'CustomUser':
            Creates and saves a superuser with the given parameters.
    """

    def create_user(self, email: str, password: str = None, **extra_fields) -> 'CustomUser':
        """
        Create and save a user with the given parameters.

        Args:
            email (str): User's email.
            password (str): User's password.
            **extra_fields (dict): Additional user fields.

        Returns:
            CustomUser: Created user.

        Raises:
            ValueError: If email is not provided.
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
        Create and save a superuser with the given parameters.

        Args:
            email (str): Superuser's email.
            password (str): Superuser's password.
            **extra_fields (dict): Additional superuser fields.

        Returns:
            CustomUser: Created superuser.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model.

    CustomUser model represents a custom user model that
    inherits AbstractBaseUser and PermissionsMixin. It is
    used to create users with unique emails instead of
    standard usernames.

    Attributes:
        email (str): User's email.
        is_staff (bool): Indicates whether the user is a staff member.
        is_active (bool): Indicates whether the user is active.
        date_joined (datetime): Date and time of user registration.

    Methods:
        email_user(self, subject: str, message: str, from_email: str = None, **kwargs):
            Sends an email to the user.
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
        Sends an email to the user.

        Args:
            subject (str): Email subject.
            message (str): Email message text.
            from_email (str, optional): Sender's email.
            **kwargs: Additional arguments for send_mail.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)
