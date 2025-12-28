from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import BlogPost


class BlogListView(ListView):
    """Отображает список опубликованных блоговых записей."""

    model = BlogPost
    template_name = "blog/list.html"
    context_object_name = "posts"

    def get_queryset(self):
        """Возвращает только опубликованные статьи."""
        return BlogPost.objects.filter(is_published=True)


class BlogDetailView(DetailView):
    """Отображает детальную информацию о блоговой записи."""

    model = BlogPost
    template_name = "blog/detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        """Увеличивает счётчик просмотров и отправляет email при достижении 100 просмотров."""
        obj = super().get_object(queryset)

        # Проверяем, достигнет ли после увеличения 100 просмотров
        if obj.views_count == 99:  # перед увеличением на 1 будет ровно 99
            send_mail(
                subject="Поздравляем! Статья набрала 100 просмотров!",
                message=f'Статья "{obj.title}" достигла 100 просмотров!\n\n'
                f"Ссылка: https://your-site.com/blogs/{obj.pk}/",
                from_email="no-reply@skystore.com",
                recipient_list=["Couguar72@gmail.com"],
                priority="now",
            )
            messages.info(self.request, "Поздравительное письмо отправлено на email!")

        # Увеличиваем счётчик
        obj.views_count += 1
        obj.save(update_fields=["views_count"])

        return obj


class BlogCreateView(LoginRequiredMixin, UserPassesTestMixin,CreateView):
    """Создаёт новую блоговую запись."""

    model = BlogPost
    template_name = "blog/create.html"
    fields = ["title", "content", "preview", "is_published"]
    success_url = reverse_lazy("blog:list")

    def test_func(self):
        return self.request.user.groups.filter(name="Контент-менеджер").exists()

    def form_valid(self, form):
        messages.success(self.request, "Статья успешно создана!")
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирует существующую блоговую запись."""

    model = BlogPost
    template_name = "blog/update.html"
    fields = ["title", "content", "preview", "is_published"]
    success_url = reverse_lazy("blog:list")  # будет переопределено ниже

    def test_func(self):
        return self.request.user.groups.filter(name="Контент-менеджер").exists()

    def get_success_url(self):
        """После успешного обновления перенаправляет на страницу просмотра статьи."""
        messages.success(self.request, "Статья успешно обновлена!")
        return reverse_lazy("blog:detail", kwargs={"pk": self.object.pk})


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаляет блоговую запись."""

    model = BlogPost
    template_name = "blog/delete.html"
    success_url = reverse_lazy("blog:list")

    def test_func(self):
        return self.request.user.groups.filter(name="Контент-менеджер").exists()

    def form_valid(self, form):
        messages.success(self.request, "Статья удалена.")
        return super().form_valid(form)
