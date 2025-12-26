from django.contrib.auth import get_user_model
from django.db import models
import uuid
import json
from apps.common.models import TimeStampedModel
from apps.common.validators import validate_nepali_mobile
from apps.orders.constants import CountryEnum, NepalDeliveryProvincesEnum, BagmatiCities, PaymentOptions, \
    PaymentStatusEnum, OrderStatusEnum, OrderStatusColors
from apps.products.models import Product
from django.urls import reverse

# Create your models here.
User = get_user_model()


class Order(TimeStampedModel, models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    ph_number = models.CharField(max_length=14, validators=[validate_nepali_mobile])
    payment_option = models.CharField(max_length=100, choices=PaymentOptions.choices, default=PaymentOptions.COD)
    note = models.TextField(blank=True, null=True)
    products = models.JSONField(null=True, blank=True)

    total_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)
    redeemed_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)

    status = models.CharField(max_length=20, choices=OrderStatusEnum.choices, default=OrderStatusEnum.PLACED)
    multiple_sellers = models.BooleanField(default=False)

    # Shipping Address
    use_billing_address = models.BooleanField(default=False)
    shipping_street = models.CharField(max_length=255, null=True, blank=True)
    shipping_country = models.CharField(max_length=100, choices=CountryEnum.choices, default=CountryEnum.NEPAL)
    shipping_region = models.CharField(max_length=100, choices=NepalDeliveryProvincesEnum.choices,
                                       default=NepalDeliveryProvincesEnum.BAGMATI)
    shipping_city = models.CharField(max_length=100, choices=BagmatiCities.choices, default=BagmatiCities.KATHMANDU)
    shipping_zip_code = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"#{self.full_name}_{int(self.created.timestamp())}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def shipping_address(self):
        return f"{self.shipping_street},{self.shipping_city}, {self.shipping_region}, {self.shipping_zip_code}, {self.shipping_country}"

    def get_absolute_url(self):
        return reverse("users:order-detail", kwargs={"uuid": self.uuid})

    @property
    def sellers(self):
        product_ids = list(self.products.keys())
        products = Product.objects.filter(pk__in=product_ids)
        sellers = products.values_list("seller", flat=True)
        return sellers

    @property
    def items(self):
        product_ids = self.products.keys()
        return Product.objects.filter(pk__in=product_ids)

    @property
    def status_with_colors(self):
        return {
            "text": self.status,
            "color": OrderStatusColors[self.status.upper()].label,
        }


class OrderStatusLog(TimeStampedModel, models.Model):
    order = models.ForeignKey(Order, related_name='status_logs', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=OrderStatusEnum.choices)
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    note = models.TextField(blank=True)

    class Meta:
        ordering = ['created']


class Transaction(TimeStampedModel, models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    is_payment_success = models.BooleanField(default=False)
    remarks = models.CharField(blank=True, null=True, max_length=255)

    def __str__(self):
        return f"#{self.uuid}"


class KhaltiTransaction(TimeStampedModel, models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name="khalti_transactions")
    pidx = models.CharField(max_length=255, unique=True)
    tidx = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, choices=PaymentStatusEnum.choices, default=PaymentStatusEnum.PENDING)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_order_id = models.CharField(max_length=255)
    purchase_order_name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255, help_text="Payer's Khalti ID", null=True, blank=True)

    def __str__(self):
        return f"Khalti Transaction {self.transaction}"


class OrderCancellation(TimeStampedModel, models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.order} Cancellation"


class SellerPayment(TimeStampedModel, models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    remarks = models.TextField(blank=True, null=True)
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_quantity = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    commission = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("transaction", "seller")

    def __str__(self):
        return f"Seller Payment to {self.seller} for {self.product_name} of {self.transaction}"