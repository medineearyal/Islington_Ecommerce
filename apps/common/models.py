from django.contrib.auth import get_user_model
from django.db import models

from apps.common.mixins import SlugMixin
from apps.common.validators import validate_nepali_mobile
from apps.orders.constants import CountryEnum, NepalDeliveryProvincesEnum, BagmatiCities

# Create your models here.
User = get_user_model()


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AddressModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="address")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    country = models.CharField(max_length=100, choices=CountryEnum.choices, default=CountryEnum.NEPAL)
    state = models.CharField(max_length=100, choices=NepalDeliveryProvincesEnum.choices,
                             default=NepalDeliveryProvincesEnum.BAGMATI)
    city = models.CharField(max_length=100, choices=BagmatiCities.choices, default=BagmatiCities.KATHMANDU)
    zip_code = models.CharField(max_length=9)
    email = models.EmailField()
    ph_number = models.CharField(max_length=20, validators=[validate_nepali_mobile, ])

    def __str__(self):
        return f"{self.user}_shipping_address"

    @property
    def address(self):
        return f"{self.street}, {self.country}, {self.city}, {self.zip_code}"


class Tag(SlugMixin, models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=False, blank=False)

    def __str__(self):
        return self.name


class Notices(SlugMixin, TimeStampedModel, models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=False, blank=True)
    header_text = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    is_active = models.BooleanField(default=False)
    image = models.ImageField(upload_to="notices", null=True, blank=True)

    def __str__(self):
        return self.name