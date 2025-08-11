from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from apps.common.mixins import SlugMixin
from apps.common.models import TimeStampedModel
from apps.products.constans import BadgeTypeEnum
from django.db.models import Q, Max
from django.utils.timezone import localtime


# Create your models here.
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
                qs = Product.objects.filter(category__in=self.children.all().values_list("pk", flat=True), is_featured=True).order_by('-discount')
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


class Product(SlugMixin, TimeStampedModel, models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.IntegerField(default=1)
    tags = models.ManyToManyField(Tag, related_name="tags")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, limit_choices_to=leaf_categories)
    slug = models.SlugField(blank=True, null=True, unique=True)
    is_featured = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to="products/thumbnails/", null=True, blank=True)
    is_header_banner = models.BooleanField(default=False)
    discount=models.PositiveSmallIntegerField(default=0)
    headline = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def discounted_price(self):
        if self.discount:
            return round(self.price - (self.price * Decimal(self.discount / 100)), 2)
        return self.price


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
    feedback = models.CharField(max_length=500)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

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