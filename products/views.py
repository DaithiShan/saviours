from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.safestring import mark_safe
from .models import Product, ProductSelect, Rating


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
        'ratings': Rating.objects.filter(product=product),
        'rating_options': [i * 20 for i in range(1,6)], 
    }

    if request.user.is_authenticated:
        # Get user rating for product or None
        try:
            context["user_rating"] = context["ratings"].get(
                user_id=request.user
            )
        except Rating.DoesNotExist:
            context["user_rating"] = None

    return render(request, 'products/product_page.html', context)


@login_required
def rate_product(request, product_id):
    """
    View for adding ratings to products
    using star buttons on product page
    """

    product = Product.objects.get(pk=product_id)
    rating = request.POST.get("star-rating")
    if rating:
        # Update existing rating or create new one
        rating_update_values = {"rating": rating}
        rating_obj, created = Rating.objects.update_or_create(
            user_id=request.user,
            product=product,
            defaults=rating_update_values,
        )
        # INFO messages redefined as a'star' in settings.py
        messages.info(request, f"Rated {int(rating) // 20} / 5 Stars!")
    return redirect(request.GET.get("next"))
