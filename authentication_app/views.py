from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, UpdateView, TemplateView

from authentication_app import forms
from authentication_app.forms import CustomAuthenticationForm


class HomeView(TemplateView):
    """
    View for displaying the home page.

    Displays the home page for users.

    Attributes:
        template_name (str): The name of the template to be displayed.

    """
    template_name = 'home.html'


class CustomLoginView(LoginView):
    """
    Custom view for user login.

    Displays the login form for users with extended authentication via email and password.

    Attributes:
        form_class (Form): The class of the user login form.

    Methods:
        form_valid(self, form): Handles successful user authentication.

    """
    form_class = CustomAuthenticationForm

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request=self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)
            messages.add_message(self.request, messages.INFO, _(f'Welcome!'))
            return super().form_valid(form)
        else:
            messages.add_message(self.request, messages.INFO, _(f'Something went wrong :('))
            return self.form_invalid(form)


class CustomLogoutView(LogoutView):
    """
    Custom view for user logout.

    Logs out the user and displays a message about successful logout.

    """

    def dispatch(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.INFO, _("See you later!"))
        return super().dispatch(request, *args, **kwargs)


class RegisterView(CreateView):
    """
    Custom view for registering a new user.

    Displays the registration form and, upon successful registration,
    automatically logs in the user.

    Attributes:
        model (Model): The user model used in the project.
        form_class (Form): The class of the user registration form.

    Methods:
        form_valid(self, form): Handles successful user registration.

    """
    model = get_user_model()
    form_class = forms.CustomUserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.add_message(self.request, messages.INFO, _(f'Successful Login!'))
        return redirect('authentication_app:home')


class ProfileEditView(UserPassesTestMixin, UpdateView):
    """
    Custom view for editing a user's profile.

    Allows users to edit their profile.

    Attributes:
        model (Model): The user model used in the project.
        form_class (Form): The class of the profile editing form.

    Methods:
        test_func(self): Checks if the current user has access to edit the profile.
        get_success_url(self): Returns the URL to redirect to after successful profile editing.

    """
    model = get_user_model()
    form_class = forms.CustomUserChangeForm

    def test_func(self):
        return True if self.request.user.pk == self.kwargs.get("pk") else False

    def get_success_url(self):
        return reverse_lazy("authentication_app:profile_edit", args=[self.request.user.pk])
