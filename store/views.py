from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from products.models import Product


def home(request):
    """
    Landing/Welcome page for website
    """
    return render(request, 'store/index.html')


def shop(request, category=None, subcategory=None):
    """
    Main shop page list of available products
    """
    context = {}
    q = Q()

    # text search
    if "q" in request.GET:
        query = request.GET.get("q")
        q &= (
            Q(title__icontains=query) |
            Q(category__title__icontains=query) |
            Q(subcategory__title__icontains=query) |
            Q(type__title__icontains=query) |
            Q(brand__name__icontains=query)
        )

    # URL parameter filters
    if subcategory:
        q &= Q(subcategory__slug=subcategory)
    elif category:
        q &= Q(category__slug=category)

    # products
    products = Product.objects.filter(q)

    # from django docs
    paginator = Paginator(products, 8)  # Show 12 products per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'category': category,
        }
    return render(request, 'store/shop.html', context)
