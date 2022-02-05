from products.models import Product, Category


def subcategories_per_category(request):
    """
    function to insert product categories,
    into base template
    """
    context = {}
    context["categories"] = Category.objects.all()
    context["category_subcategories"] = {}
    for category in context["categories"]:
        context["category_subcategories"][category] = sorted(set(
            Product.objects.filter(category=category).values_list(
                "subcategory__title", flat=True
            )
        ))
    return context
