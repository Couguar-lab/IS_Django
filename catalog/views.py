from django.shortcuts import render, get_object_or_404, redirect

from catalog.models import Product, Contacts, Category
from django.core.paginator import Paginator


def home(request):
    products_list = Product.objects.all().order_by('-created_at')
    paginator = Paginator(products_list, 6)  # 6 товаров на страницу
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(request, 'catalog/home.html', {'products': products})

def contacts(request):
    success = False
    if request.method == 'POST':
        success = True
    contacts = Contacts.objects.first()  # предполагаем, что один объект
    return render(request, 'catalog/contacts.html', {
        'success': success,
        'contacts': contacts
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})


def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        category_id = request.POST['category']
        category = Category.objects.get(pk=category_id)

        Product.objects.create(
            name=name,
            description=description,
            price=price,
            category=category
        )
        return redirect('catalog:home')

    categories = Category.objects.all()
    return render(request, 'catalog/add_product.html', {'categories': categories})