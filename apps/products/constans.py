from django.db.models import TextChoices


class BadgeTypeEnum(TextChoices):
    HOT = "hot", "HOT"
    BEST_DEALS = "best_deals", "BEST DEALS"
    FRESH = "fresh", "FRESH"
    DISCOUNT = "discount", "OFF"