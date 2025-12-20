from django.views.generic import ListView, DetailView, TemplateView
from django.contrib import messages
from .models import Product, Contacts
from django.views.generic import CreateView
from django.urls import reverse_lazy

class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 6
    ordering = ['-created_at']

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = Contacts.objects.first()
        return context

    def post(self, request, *args, **kwargs):
        messages.success(request, "Спасибо! Ваше сообщение отправлено.")
        return self.get(request, *args, **kwargs)

class AddProductView(CreateView):
    model = Product
    template_name = 'catalog/add_product.html'
    fields = ['name', 'description', 'image', 'category', 'price']
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        messages.success(self.request, "Товар успешно добавлен!")
        return super().form_valid(form)