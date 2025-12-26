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
    CANCELED = "canceled", "Canceled"

class OrderStatusDescription(TextChoices):
    PLACED = "placed", "Your order has been placed."
    SHIPPED = "shipped", "Your order has been shipped."
    OUT_FOR_DELIVERY = "out_for_delivery", "Your order has been sent out for delivery."
    DELIVERED = "delivered", "Thank You! for your patience, your order has been successfully delivered."
    CANCELED = "canceled", "Your Delivery has been canceled."

class OrderStatusColors(TextChoices):
    PLACED = "placed", "var(--clr-gray-700)"
    SHIPPED = "shipped", "var(--clr-warning-500)"
    OUT_FOR_DELIVERY = "out_for_delivery", "var(--clr-secondary-500)"
    DELIVERED = "delivered", "var(--clr-success-500)"
    CANCELED = "canceled", "var(--clr-danger-500)"