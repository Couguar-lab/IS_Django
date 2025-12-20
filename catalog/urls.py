from django.urls import path
from .views import HomeView, ProductDetailView, ContactsView, AddProductView

app_name = 'catalog'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('add-product/', AddProductView.as_view(), name='add_product'),
]