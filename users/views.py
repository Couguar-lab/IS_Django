from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from django.views.generic import UpdateView

from .forms import CustomUserCreationForm
from .models import CustomUser


class CustomLoginView(LoginView):
    """Авторизация по email."""

    template_name = "users/login.html"
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    """Выход пользователя с редиректом на главную."""

    def get_next_page(self):
        return reverse("catalog:home")


class RegisterView(CreateView):
    """Регистрация нового пользователя."""

    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)

        # Приветственное письмо
        send_mail(
            subject="Добро пожаловать в Skystore!",
            message=f"Привет, {user.username}! Спасибо за регистрацию.",
            from_email="no-reply@skystore.com",
            recipient_list=[user.email],
        )
        messages.success(self.request, "Регистрация успешна! Проверьте email.")
        return response


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля авторизованного пользователя."""

    model = CustomUser
    fields = ["avatar", "phone", "country"]
    template_name = "users/profile.html"
    success_url = reverse_lazy("catalog:home")

    def get_object(self, queryset=None):
        """Возвращает текущего пользователя."""
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Профиль успешно обновлён!")
        return super().form_valid(form)
