from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from mptt.models import MPTTModel, TreeForeignKey
from apps.common.mixins import SlugMixin
from apps.common.models import TimeStampedModel
from apps.products.constans import BadgeTypeEnum, ProductInventoryStatusEnum, ProductColorsEnum, ProductAttributesEnum
from django.db.models import Q, Max, Avg
from django.utils.timezone import localtime


# Create your models here.
User = get_user_model()

class Category(SlugMixin, MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children"
    )
    image = models.ImageField(upload_to="categories/", null=True, blank=True)
    slug = models.SlugField(blank=True, null=True, unique=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    @property
    def featured_products(self):
        qs = Product.objects.filter(category=self, is_featured=True)

        if not qs.exists():
            if not self.is_leaf_node():
                qs = Product.objects.filter(category__in=self.children.all().values_list("pk", flat=True),
                                            is_featured=True).order_by('-discount')
        return qs[:3]

    @property
    def header_banner_product(self):
        qs = Product.objects.filter(category=self)
        max_discount = qs.aggregate(Max("discount"))["discount__max"] or 0
        qs = qs.filter(discount__gte=max_discount)

        if not qs.exists():
            return Product.objects.filter(discount__gt=0).order_by("-discount").first()
        return qs.first()

class Tag(SlugMixin, models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=False, blank=False)

    def __str__(self):
        return self.name


def leaf_categories():
    return Q(children__isnull=True)

class ProductColors(models.Model):
    name = models.CharField(max_length=255)
    color_code = models.CharField(max_length=50)
    color_format = models.CharField(choices=ProductColorsEnum.choices, max_length=50)

    def __str__(self):
        return self.name


class Product(SlugMixin, TimeStampedModel, models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=1)
    tags = models.ManyToManyField(Tag, related_name="tags")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, limit_choices_to=leaf_categories, related_name="product_category")
    slug = models.SlugField(blank=True, null=True, unique=True)
    is_featured = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to="products/thumbnails/", null=True, blank=True)
    is_header_banner = models.BooleanField(default=False)
    discount = models.PositiveSmallIntegerField(default=0)
    headline = models.CharField(max_length=255, null=True, blank=True)

    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    sku = models.CharField(max_length=50, unique=True, blank=True)
    colors = models.ManyToManyField(ProductColors, related_name="colors", blank=True)

    def __str__(self):
        return self.name

    @property
    def discounted_price(self):
        if self.discount:
            return round(self.price - (self.price * Decimal(self.discount / 100)), 2)
        return self.price

    @property
    def overall_ratings(self):
        review_qs = ProductReview.objects.filter(product=self)
        average_ratings = review_qs.aggregate(Avg("rating"))["rating__avg"] or 0
        no_of_ratings = review_qs.count()
        return {
            "ratings": round(average_ratings),
            "count": no_of_ratings
        }

    @property
    def is_available(self):
        if self.stock > 0:
            return ProductInventoryStatusEnum.AVAILABLE.label, True
        else:
            return ProductInventoryStatusEnum.SOLD_OUT.label, False

class ProductDescription(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="descriptions")
    title = models.CharField(max_length=255)
    description = CKEditor5Field()

    def __str__(self):
        return f"{self.product}_{self.title}"

class Attribute(models.Model):
    name = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    datatype = models.CharField(max_length=20, choices=ProductAttributesEnum.choices)

    def __str__(self):
        return f"{self.name}"

class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name="attributes")
    value = models.TextField()

    def __str__(self):
        return f"{self.attribute.name}-{self.product}-{self.pk}"

class ProductBanner(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    short_title = models.CharField(max_length=255)
    is_display = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product}_Banner"


class Badge(models.Model):
    name = models.CharField(choices=BadgeTypeEnum.choices, max_length=255)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.product.name}_{self.name}"


class ProductImage(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField(upload_to="media/products/")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        creating = self.pk is None

        if not self.name and not creating:
            self.name = f"{self.product.name}_{self.pk}"

        super().save(*args, **kwargs)

        if creating and not self.name:
            self.name = f"{self.product.name}_{self.pk}"
            super().save(update_fields=['name'])


class ProductReview(TimeStampedModel, models.Model):
    rating = models.PositiveSmallIntegerField(default=0)
    feedback = models.TextField()
    review_from = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="reviews", null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")

    def __str__(self):
        return f"{self.product}_{self.rating}"


class BestDeals(TimeStampedModel, models.Model):
    products = models.ManyToManyField(Product, related_name="best_deals")
    is_active = models.BooleanField(default=False)
    end_date = models.DateTimeField()

    def __str__(self):
        return f"Best Deals_{self.created}_{self.is_active}"

    def clean(self):
        if self.is_active:
            qs = BestDeals.objects.filter(is_active=True).exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError(f"Only one Best Deal is allowed at a time.")

    @property
    def iso_end_date(self):
        return localtime(self.end_date).isoformat()
