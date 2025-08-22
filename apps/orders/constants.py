from django.db.models import TextChoices


class CountryEnum(TextChoices):
    NEPAL = "np", "Nepal"


class NepalDeliveryProvincesEnum(TextChoices):
    BAGMATI = "bagmati", "Bagmati"

class NepalProvinceEnum(TextChoices):
    BAGMATI = "bagmati", "Bagmati"
    GANDAKI = "gandaki", "Gandaki"
    KARNALI = "karnali", "Karnali"
    KOSHI = "koshi", "Koshi"
    MADESH = "madesh", "Madesh"
    LUMBINI = "lumbinini", "Lumbinini"
    SUDURPASCHIM = "sudurpaschim", "Sudurpaschim"


class BagmatiCities(TextChoices):
    KATHMANDU = "kathmandu", "Kathmandu"
    BHAKTAPUR = "bhaktapur", "Bhaktapur"
    LALITPUR = "lalitpur", "Lalitpur"


class PaymentOptions(TextChoices):
    COD = "cod", "Cash on Delivery"
    KHALTI = "khalti", "Khalti"
    QR = "qr", "QR"


class PaymentStatusEnum(TextChoices):
    PENDING = "pending", "Pending"
    COMPLETED = "completed", "Completed"
    CANCELED = "canceled", "User canceled"


class OrderStatusEnum(TextChoices):
    PLACED = "placed", "Placed"
    SHIPPED = "shipped", "Shipped"
    OUT_FOR_DELIVERY = "out_for_delivery", "Out For Delivery"
    DELIVERED = "delivered", "Delivered"