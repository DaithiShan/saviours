from django.shortcuts import render
from django.core.paginator import Paginator
from products.models import Product


def home(request):
    """
    Landing/Welcome page for website
    """
    return render(request, 'store/index.html')


def shop(request):
    """
    Main shop page list of available products
    """
    products = Product.objects.all()

    # from django docs
    paginator = Paginator(products, 8)  # Show 12 products per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj
        }
    return render(request, 'store/shop.html', context)
