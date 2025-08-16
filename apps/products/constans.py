from django.db.models import TextChoices

class BadgeTypeEnum(TextChoices):
    HOT = "hot", "HOT"
    BEST_DEALS = "best_deals", "BEST DEALS"
    FRESH = "fresh", "FRESH"
    DISCOUNT = "discount", "OFF"

class ShopSortChoicesEnum(TextChoices):
    POPULAR = "popular", "Most Popular"
    PRICE_DESC = "price-descend", "Price (High to Low)"
    PRICE_ASC = "price-ascend", "Price (Low to High)"
    AZ = "a-z", "A-Z"
    ZA = "z-a", "Z-A"

class ProductInventoryStatusEnum(TextChoices):
    AVAILABLE = "is-available", "In Stock"
    SOLD_OUT = "sold-out", "Sold Out"

class ProductColorsEnum(TextChoices):
    HEX = "hex", "Hex"
    RGB = "rgb", "RGB"
    RGBA = "rgba", "RGBA"
    HSL = "hsl", "HSL"

class ProductAttributesEnum(TextChoices):
    INT = "int", "Integer"
    FLOAT = "float", "Float"
    STR = "str", "String"
    BOOL = "bool", "Boolean"