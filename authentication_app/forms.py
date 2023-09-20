from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating a custom user account (registration).

    This is a customizable user registration form that includes an email
    input field instead of the default username input field.

    Attributes:
        email (forms.EmailField): Field for entering an email address.
        field_order (list): The order of fields in the form.

    Meta:
        model (Model): The user model used in the project.
        fields (tuple): Fields included in the form (email, password1, password2).

    """
    email: forms.EmailField = forms.EmailField(required=True)
    field_order: list = [
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
    Form for changing user account data.

    This form allows users to change their email address.

    Meta:
        model (Model): The user model used in the project.
        fields (tuple): Fields that can be changed (email).

    """

    class Meta:
        model = get_user_model()
        fields = (
            "email",
        )


class CustomAuthenticationForm(AuthenticationForm):
    """
    Form for authenticating (logging in) users.

    This form extends the standard `AuthenticationForm` with an email input
    field instead of the default username input field.

    Attributes:
        email (forms.EmailField): Field for entering an email address.
        password (forms.CharField): Field for entering a password.

    """
    email: forms.EmailField = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': True, 'autocomplete': 'email'}),
        label="Email"
    )
    password: forms.CharField = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'current-password'}),
        strip=False,
        label="Password"
    )
    field_order: list = ['email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "username" in self.fields:
            del self.fields["username"]
