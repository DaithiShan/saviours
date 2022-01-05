from django.db import models
from django.template.defaultfilters import slugify
from PIL import Image

from accounts.models import Account


# ------ Product Categories ------


class Category(models.Model):
    """
    Defines category of selected product
     (for filtering purposes)
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    ordering = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ("ordering", "title")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Overwrite default save and create product slug
        """
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Subcategory(models.Model):
    """
    Defines subcategory of selected product
     (for filtering purposes)
    """
    parent = models.ForeignKey(Category,
                               related_name='subcategories',
                               blank=True,
                               null=True,
                               on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, null=True)
    ordering = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Subcategories"
        ordering = ("parent", "ordering", "title")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


# ------ Products ------


class Product(models.Model):
    """ Defines all products """
    category = models.ForeignKey(Category,
                                 blank=True,
                                 null=True,
                                 related_name='products',
                                 on_delete=models.SET_NULL)
    subcategory = models.ForeignKey(Subcategory,
                                    blank=True,
                                    null=True,
                                    related_name='subcategory',
                                    on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    stock = models.IntegerField(default=15)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="media/", blank=True, null=True)
    thumbnail = models.ImageField(
        upload_to="media/thumbnails/", blank=True, null=True
    )

    class Meta:
        """
        Products sorted by name
        ref: https://tinyurl.com/3v38mtn5
        """
        ordering = ['title']

    def __str__(self):
        return self.title


# ------ Product Ratings ------


class Rating(models.Model):
    user_id = models.ForeignKey(
        Account, related_name="ratings", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="ratings", on_delete=models.CASCADE
    )

    class Stars(models.IntegerChoices):
        ONE = 20, "★☆☆☆☆"
        TWO = 40, "★★☆☆☆"
        THREE = 60, "★★★☆☆"
        FOUR = 80, "★★★★☆"
        FIVE = 100, "★★★★★"

    rating = models.IntegerField(choices=Stars.choices)
    date_added = models.DateTimeField(
        verbose_name="date added", auto_now_add=True
    )

    class Meta:
        verbose_name_plural = "Ratings"
        ordering = ("date_added", "user_id")

    def __str__(self):
        return f"{self.user_id}: {self.product}"
