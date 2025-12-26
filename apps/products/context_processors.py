def cart_total_sum(request):
    cart = request.session.get('cart', {})
    total = sum(
        [
            int(item["quantity"]) * float(item["price"]
            if not item["discount"] else item["discounted_price"])
            for item in cart.values()
        ]
    )
    return {"cart_sum": total}
