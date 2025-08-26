from django.shortcuts import get_object_or_404

from apps.products.models import Product


def process_cart_totals(cart):
    """
    This utility function Calculates the necessary totals from the cart items stored in the session.
    Args:
        cart: cart dictionary
    Returns:
        total_sum, vat_amount, dst_amount, total_sellers
    """
    sellers = set()

    for pid, item in cart.items():
        product = get_object_or_404(Product, pk=int(pid))
        sellers.add(product.seller_id)

        if item["discount"]:
            item["total_price"] = item["discounted_price"] * item["quantity"]
            item["vat_amount"] = 0.13 * item["discounted_price"]

            if item["category"] == "Digital Service":
                item["digital_service_tax"] = 0.02 * item["discounted_price"]
        else:
            item["total_price"] = item["price"] * item["quantity"]
            item["vat_amount"] = 0.13 * item["price"]

            if item["category"] == "Digital Service":
                item["digital_service_tax"] = 0.02 * item["price"]

    total_sum = sum(item["total_price"] for _, item in cart.items())
    # TODO: VAT Amount Might Change
    # TODO: Need to Handle Coupon To Give Certain Discount On The Overall Total
    vat_amount = sum(item["vat_amount"] for _, item in cart.items())
    dst_amount = sum(item["digital_service_tax"] for _, item in cart.items() if hasattr(item, "digital_service_tax"))

    return total_sum, vat_amount, dst_amount, len(sellers)
