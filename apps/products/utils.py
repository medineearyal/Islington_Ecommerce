from django.db.models import Q

from apps.products.models import Product


def generate_unique_sku(category, product_code, *variants):
    """
    Generate a unique SKU for Django model, checking against existing SKUs.
    Format: CAT-###-VAR1-VAR2[-N]
    """
    category = str(category).upper().replace(" ", "")
    code = str(product_code).zfill(3)
    variants = [str(v).upper().replace(" ", "") for v in variants]

    base_sku = "-".join([category, code] + variants)
    sku = base_sku
    counter = 1

    # Check for existing SKUs in DB
    while Product.objects.filter(sku=sku).exists():
        sku = f"{base_sku}-{counter}"
        counter += 1

    return sku