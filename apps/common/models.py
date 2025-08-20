from django.contrib.auth import get_user_model
from django.db import models

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    country = models.CharField(max_length=100, choices=CountryEnum.choices, default=CountryEnum.NEPAL)
    state = models.CharField(max_length=100, choices=NepalDeliveryProvincesEnum.choices,
                             default=NepalDeliveryProvincesEnum.BAGMATI)
    city = models.CharField(max_length=100, choices=BagmatiCities.choices, default=BagmatiCities.KATHMANDU)
    zip_code = models.CharField(max_length=9)
    email = models.EmailField()
    ph_number = models.TextField(max_length=20, validators=[validate_nepali_mobile, ])

    def __str__(self):
        return f"{self.user}_shipping_address"
