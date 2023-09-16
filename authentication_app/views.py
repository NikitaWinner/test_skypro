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
    Представление для отображения домашней страницы.

    Отображает домашнюю страницу для пользователей.

    Attributes:
        template_name (str): Имя шаблона для отображения.

    """
    template_name = 'home.html'


class CustomLoginView(LoginView):
    """
    Пользовательское представление для входа (логина) пользователя.

    Отображает форму входа (логина) для пользователей с расширенной
    аутентификацией через email и пароль.

    Attributes:
        form_class (Form): Класс формы входа пользователя.

    Methods:
        form_valid(self, form): Обрабатывает успешную аутентификацию пользователя.

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
    Пользовательское представление для выхода (логаута) пользователя.

    Выполняет выход пользователя и отображает сообщение об успешном выходе.

    """

    def dispatch(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.INFO, _("See you later!"))
        return super().dispatch(request, *args, **kwargs)


class RegisterView(CreateView):
    """
    Пользовательское представление для регистрации нового пользователя.

    Отображает форму регистрации и, при успешной регистрации,
    выполняет автоматический вход пользователя.

    Attributes:
        model (Model): Модель пользователя, используемая в проекте.
        form_class (Form): Класс формы регистрации пользователя.

    Methods:
        form_valid(self, form): Обрабатывает успешную регистрацию пользователя.

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
    Пользовательское представление для редактирования профиля пользователя.

    Позволяет пользователям редактировать свой профиль.

    Attributes:
        model (Model): Модель пользователя, используемая в проекте.
        form_class (Form): Класс формы редактирования профиля.

    Methods:
        test_func(self): Проверяет, имеет ли текущий пользователь доступ к редактированию профиля.
        get_success_url(self): Возвращает URL-адрес для перенаправления после успешного редактирования профиля.

    """
    model = get_user_model()
    form_class = forms.CustomUserChangeForm

    def test_func(self):
        return True if self.request.user.pk == self.kwargs.get("pk") else False

    def get_success_url(self):
        return reverse_lazy("authentication_app:profile_edit", args=[self.request.user.pk])
