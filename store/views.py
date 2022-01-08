from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from urllib.parse import urlparse, urlunparse
from django.http import QueryDict
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

    # product
    order = request.GET.get("order_by") or "ordering"
    products = Product.objects.filter(q).order_by(order)

    # Pagination object from django docs
    paginator = Paginator(products, 4)  # Show 8 products per page.
    page_number = request.GET.get('page')
    context["page_obj"] = paginator.get_page(page_number)

    # Product List
    context["products"] = products

    # Category & Subcategory
    context["category"] = category
    context["subcategory"] = subcategory

    return render(request, 'store/shop.html', context)
