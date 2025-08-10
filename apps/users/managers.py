from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class AuthUserManager(BaseUserManager):
    """
    Auth User Model Manager where email is the unique identifier of the user
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and Save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email Must Be Set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and Save a Superuser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)
