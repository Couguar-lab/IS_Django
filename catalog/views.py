from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import ProductForm
from .models import Contacts, Product


class HomeView(ListView):
    """Отображает главную страницу с пагинированным списком продуктов."""

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"
    paginate_by = 6
    ordering = ["-created_at"]


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Отображает детальную информацию о конкретном продукте."""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ContactsView(TemplateView):
    """Отображает страницу контактов и обрабатывает отправку формы обратной связи."""

    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):
        """Добавляет в контекст первые контактные данные компании."""
        context = super().get_context_data(**kwargs)
        context["contacts"] = Contacts.objects.first()
        return context

    def post(self, request, *args, **kwargs):
        """Обрабатывает POST-запрос формы и показывает сообщение об успехе."""
        messages.success(request, "Спасибо! Ваше сообщение отправлено.")
        return self.get(request, *args, **kwargs)


class AddProductView(LoginRequiredMixin, CreateView):
    """Позволяет добавить новый продукт через форму."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/add_product.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        """Показывает сообщение об успешном добавлении продукта."""
        form.instance.owner = self.request.user
        form.instance.is_published = False  # по умолчанию не опубликован
        messages.success(self.request, "Товар успешно добавлен и отправлен на модерацию!")
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирует существующий продукт через форму."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_update.html"
    success_url = reverse_lazy("catalog:home")

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner or self.request.user.has_perm("catalog.can_unpublish_product")

    def form_valid(self, form):
        """Показывает сообщение об успешном обновлении продукта."""
        messages.success(self.request, "Товар успешно обновлён!")
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаляет продукт с подтверждением."""

    model = Product
    template_name = "catalog/product_delete.html"
    success_url = reverse_lazy("catalog:home")

    def test_func(self):
        product = self.get_object()
        return (self.request.user == product.owner or
                self.request.user.has_perm("catalog.delete_product") or
                self.request.user.has_perm("catalog.can_unpublish_product"))

    def form_valid(self, form):
        """Показывает сообщение об успешном удалении продукта."""
        messages.success(self.request, "Товар успешно удалён.")
        return super().form_valid(form)
