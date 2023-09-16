from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.forms import AuthenticationForm


class CustomUserCreationForm(UserCreationForm):
    """
    Форма для создания пользовательской учетной записи (регистрации).

    Это настраиваемая форма для регистрации пользователей, которая
    включает в себя поле для ввода email вместо стандартного поля
    для ввода имени пользователя (username).

    Attributes:
        email (forms.EmailField): Поле для ввода email.
        field_order (list): Порядок полей в форме.

    Meta:
        model (Model): Модель пользователя, используемая в проекте.
        fields (tuple): Поля, которые включены в форму (email, password1, password2).

    """
    email = forms.EmailField(required=True)
    field_order = [
        "email",
        "password1",
        "password2",
    ]

    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "password1",
            "password2",
        )


class CustomUserChangeForm(forms.ModelForm):
    """
    Форма для изменения данных пользовательской учетной записи.

    Эта форма позволяет пользователям изменять свой email.

    Meta:
        model (Model): Модель пользователя, используемая в проекте.
        fields (tuple): Поля, которые можно изменять (email).

    """

    class Meta:
        model = get_user_model()
        fields = (
            "email",
        )


class CustomAuthenticationForm(AuthenticationForm):
    """
    Форма аутентификации (логина) пользователей.

    Эта форма расширяет стандартную форму аутентификации `AuthenticationForm`,
    добавляя поле для ввода email вместо стандартного поля для ввода имени
    пользователя (username).

    Attributes:
        email (forms.EmailField): Поле для ввода email.
        password (forms.CharField): Поле для ввода пароля.

    """
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': True, 'autocomplete': 'email'}),
        label="Email"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'current-password'}),
        strip=False,
        label="Пароль"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "username" in self.fields:
            del self.fields["username"]
