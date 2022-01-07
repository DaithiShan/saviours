from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Product, ProductSelect


# ------ Product Page ------


def product_page(request, category, subcategory, product):
    """
    Returns specified product
    """
    product = get_object_or_404(Product, slug=product)
    product_options = product.product_select.all()

    # gets the product variations to select
    product_select = ProductSelect.objects.filter(
        product_select=product_options,
        product=product)
    product_selected = product_select

    context = {
        'product': product,
        'product_options': product_options,
        'product_selected': product_selected,
    }

    return render(request, 'products/product_page.html', context)
