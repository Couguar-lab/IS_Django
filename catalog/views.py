from django.shortcuts import render

from catalog.models import Product, Contacts


def home(request):
        latest_products = Product.objects.order_by('-created_at')[:5]
        print("Последние 5 продуктов:")  # в консоль
        for p in latest_products:
            print(f"- {p.name} ({p.price} руб.)")
        return render(request, 'catalog/home.html', {'latest_products': latest_products})

def contacts(request):
    success = False
    if request.method == 'POST':
        success = True
    contacts = Contacts.objects.first()  # предполагаем, что один объект
    return render(request, 'catalog/contacts.html', {
        'success': success,
        'contacts': contacts
    })