from django.shortcuts import render
from products.models import Product


def home(request):
    return render(request, 'store/index.html')


def shop(request):
    products = Product.objects.all()
    context = {
        'products': products
        }
    return render(request, 'store/shop.html', context) 
