from django.core.cache import cache
from .models import Product

def get_products_by_category(category_id: int):
    """Возвращает список продуктов в указанной категории с низкоуровневым кешированием."""
    cache_key = f"products_category_{category_id}"
    products = cache.get(cache_key)

    if products is None:
        products = Product.objects.filter(category_id=category_id, is_published=True).select_related("category")
        cache.set(cache_key, products, timeout=60 * 15)  # 15 минут

    return products