from django.shortcuts import get_object_or_404, render

from .models import Product


# Create your views here.
def products(request):
    all_products = Product.objects.all()
    return render(request, "products/products1.html", {"products": all_products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "products/details1.html", {"product": product})
