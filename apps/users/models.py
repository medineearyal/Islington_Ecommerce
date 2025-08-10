from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.managers import AuthUserManager


# Create your models here.
class AuthUser(AbstractUser):
    email = models.EmailField(_("Email Address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = AuthUserManager()

    def __str__(self):
        return self.email
