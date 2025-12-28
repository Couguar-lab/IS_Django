from django.urls import path

from .views import (
    AddProductView,
    ContactsView,
    HomeView,
    ProductDeleteView,
    ProductDetailView,
    ProductUpdateView, ProductsByCategoryView,
)

app_name = "catalog"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("add-product/", AddProductView.as_view(), name="add_product"),
    path(
        "products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"
    ),
    path(
        "products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"
    ),
    path("category/<int:category_id>/", ProductsByCategoryView.as_view(), name="products_by_category"),
]
