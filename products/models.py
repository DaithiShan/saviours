from django.db import models
from django.template.defaultfilters import slugify
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator


from accounts.models import Account

# Custom models adapted from https://github.com/cjcon90/the_rhythm_box/

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


# ------ Product Options ------

class ProductOption(models.Model):
    """
    Defines options available for each product:
    course times and apparel sizes
    """
    product_option = models.CharField(max_length=255)
    option_name = models.CharField(max_length=255, default='senior')

    def __str__(self):
        return str(self.product_option)

    def get_time_name(self):
        return str(self.option_name)


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
    product_select = models.ManyToManyField(ProductOption,
                                            through='ProductSelect',
                                            related_name='product_options',
                                            blank=True)
    title = models.CharField(max_length=255)
    ordering = models.IntegerField(default=0)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    thumbnail = models.ImageField(
        upload_to="products/thumbnails/", blank=True, null=True
    )

    class Meta:
        """
        Products sorted by title
        ref: https://tinyurl.com/3v38mtn5
        """
        ordering = ("ordering", "title")

    def __str__(self):
        return self.title

    def make_thumbnail(self, image, size=(250, 250)):
        """
        Method which automatically makes thumbnail images
        of the main uploaded image, reducing size to 300x300
        """
        img = Image.open(image)
        img.convert("RGB")
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, "JPEG", quality=85)
        thumbnail = File(thumb_io, name=image.name.replace("products/", ""))
        return thumbnail

    def save(self, *args, **kwargs):
        """
        Modified save method to update thumbnail only if object is
        new, or the object image has been updated
        """
        if self.pk is None:
            self.thumbnail = self.make_thumbnail(self.image)
        else:
            original = Product.objects.get(id=self.pk)
            if original.image != self.image:
                self.thumbnail = self.make_thumbnail(self.image)
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_average_rating(self):
        """
        Returns the average of all ratings existing for
        this product in their original value (/100)
        """
        ratings = Rating.objects.filter(product=self).aggregate(
            rating_avg=Avg("rating")
        )
        return (ratings["rating_avg"]) or 0

    def get_average_rating_decimal(self):
        """
        Returns the average of all ratings existing for
        this product out of /5 (for use in star ratings)
        """
        ratings = Rating.objects.filter(product=self).aggregate(
            rating_avg=Avg("rating")
        )
        return self.get_average_rating() / 20

    def get_rating_count(self):
        """
        counts how many ratings completes on this product
        """
        return Rating.objects.filter(product=self).count()

    def get_product_url(self):
        """
        Creates a redirect url for product
        based on whether products has a set type or not
        """
        url = f"/shop/{self.category.slug}/{self.subcategory.slug}/"
        return (
            url + f"{self.slug}"
        )


# ------ ManyToMany Through Table ------


class ProductSelect(models.Model):
    """
    Establishes relationship between Product and Product Options.
    Counts stock
    """
    product_select = models.ForeignKey(ProductOption,
                                       on_delete=models.CASCADE,
                                       related_name='product_selected')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='product_options')
    stock_count = models.IntegerField(default=15)

    def __str__(self):
        return str(self.product_select)

    def get_product(self):
        return str(self.product)


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
