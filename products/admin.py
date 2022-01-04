from django.contrib import admin
from .models import Category, Subcategory, Product, Rating


class CategoryAdmin(admin.ModelAdmin):
    """ Create admin views for Categories """
    list_display = ("title", "ordering")
    search_fields = ("title", "ordering")


class SubcategoryAdmin(admin.ModelAdmin):
    """ Create admin views for Subcategories """
    list_display = ("title", "parent", "ordering")
    search_fields = ("title", "parent__title", "ordering")


class ProductAdmin(admin.ModelAdmin):
    """ Create admin views for Products """
    list_display = (
        "title",
        "category",
        "subcategory",
        "price",
        "stock",
        "date_added",
    )
    search_fields = (
        "title",
        "category__title",
        "subcategory__title",
        "description",
    )
    readonly_fields = ("slug", "thumbnail", "date_added")


class RatingAdmin(admin.ModelAdmin):
    """ Create admin views for Ratings """
    list_display = ("user_id", "product", "rating", "date_added")
    search_fields = (
        "user_id__email",
        "user_id__first_name",
        "user_id__last_name",
        "product__title",
    )


# Register Category, Subcategory and Product models
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Rating, RatingAdmin)
