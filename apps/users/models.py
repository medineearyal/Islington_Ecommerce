from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.validators import validate_nepali_mobile
from apps.users.constants import UserTypeEnum
from apps.users.managers import AuthUserManager


# Create your models here.
class AuthUser(AbstractUser):
    email = models.EmailField(_("Email Address"), unique=True)
    ph_number = models.CharField(max_length=20, validators=[validate_nepali_mobile])
    profile_picture = models.ImageField(upload_to="user/profile/", null=True, blank=True)

    user_type = models.CharField(choices=UserTypeEnum.choices, max_length=20, default=UserTypeEnum.USER)

    seller_shop_logo = models.ImageField(upload_to="user/seller/profile/", null=True, blank=True)
    seller_qr_code = models.ImageField(upload_to="user/profile/", null=True, blank=True)
    seller_bank_name = models.CharField(max_length=255, null=True, blank=True)
    seller_bank_account_number = models.CharField(max_length=255, null=True, blank=True)
    seller_bank_branch_name = models.CharField(max_length=255, null=True, blank=True)
    seller_bank_account_name = models.CharField(max_length=255, null=True, blank=True)
    is_verified_seller = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = AuthUserManager()

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def billing_address(self):
        from apps.common.models import AddressModel

        try:
            address = AddressModel.objects.get(pk=self.pk)
            return address
        except AddressModel.DoesNotExist:
            return None