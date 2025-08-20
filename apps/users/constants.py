from django.db.models import TextChoices


class UserTypeEnum(TextChoices):
    USER = "user", "User"
    SELLER = "seller", "Seller"
