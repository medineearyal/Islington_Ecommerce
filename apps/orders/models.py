from django.contrib.auth import get_user_model
from django.db import models
import uuid
from apps.common.models import TimeStampedModel
from apps.common.validators import validate_nepali_mobile
from apps.orders.constants import CountryEnum, NepalDeliveryProvincesEnum, BagmatiCities, PaymentOptions, PaymentStatusEnum
from apps.products.models import Product

# Create your models here.
User = get_user_model()


class Order(TimeStampedModel, models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    ph_number = models.CharField(max_length=14, validators=[validate_nepali_mobile])
    payment_option = models.CharField(max_length=100, choices=PaymentOptions.choices, default=PaymentOptions.COD)
    note = models.TextField(blank=True, null=True)
    products = models.ManyToManyField(Product)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Shipping Address
    use_billing_address = models.BooleanField(default=False)
    shipping_street = models.CharField(max_length=255, null=True, blank=True)
    shipping_country = models.CharField(max_length=100, choices=CountryEnum.choices, default=CountryEnum.NEPAL)
    shipping_region = models.CharField(max_length=100, choices=NepalDeliveryProvincesEnum.choices, default=NepalDeliveryProvincesEnum.BAGMATI)
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

