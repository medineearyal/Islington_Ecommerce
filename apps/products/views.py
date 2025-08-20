from babel.numbers import format_decimal
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.views.generic import TemplateView, DetailView
from rest_framework.views import APIView

from .models import Product


# Create your views here.
class ProductDetailView(DetailView):
    template_name = "products/detail.html"
    context_object_name = "product"

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        reviews = product.reviews.all().order_by("-created")

        related_categories = [child.pk for child in product.category.parent.get_children()]
        related_products = Product.objects.filter(category__pk__in=related_categories).exclude(pk=product.pk)

        paginator = Paginator(reviews, 5)

        try:
            page_number = int(self.request.GET.get("page"))
            all_reviews_so_far = reviews[:page_number * paginator.per_page]
            page = paginator.get_page(page_number)

            context = {
                "page": page,
                "reviews_so_far": all_reviews_so_far,
                "product": product,
            }

            if page_number:
                return render(request, "partials/products/reviews_list.html", context)

            return render(request, self.template_name, context=context)

        except TypeError:
            all_reviews_so_far = reviews[:1 * paginator.per_page]
            page = paginator.get_page(1)

            context = {
                "reviews_so_far": page,
                "page": page,
                "product": product,
                "related_products": related_products,
            }

            return render(request, self.template_name, context=context)

    def get_object(self, queryset=None):
        return get_object_or_404(
            Product.objects.prefetch_related(
                "product_image",
                "colors",
                "attribute_set__attributes",
                "descriptions"
            ), slug=self.kwargs["slug"])


class CartView(TemplateView):
    template_name = "partials/products/cart.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        action = request.GET.get("action")
        product_id = kwargs.get("pk")
        cart = request.session.get("cart", {})
        quantity = request.GET.get("quantity")

        if action == "add":
            product = get_object_or_404(Product, id=product_id)

            if str(product_id) in cart:
                if quantity:
                    cart[str(product_id)]["quantity"] += int(quantity)
                else:
                    cart[str(product_id)]["quantity"] += 1
            else:
                cart[str(product_id)] = {
                    "name": product.name,
                    "quantity": int(quantity) if quantity else 1,
                    "price": float(product.price),
                    "discounted_price": float(product.discounted_price),
                    "discount": product.discount,
                    "thumbnail": product.thumbnail.url,
                    "stock": product.stock,
                    "category": product.category.name,
                }
            request.session["cart"] = cart
        elif action == "remove":
            cart = request.session.get("cart")
            cart.pop(str(product_id), None)
            request.session["cart"] = cart
        elif action == "update":
            if str(product_id) in cart:
                if cart[str(product_id)]["quantity"] != quantity:
                    cart[str(product_id)]["quantity"] = quantity

        total_price = sum(
            [int(item["quantity"]) * float(item["price"] if not item["discount"] else item["discounted_price"]) for item
             in cart.values()])

        extra_update_html = f"""
        <span id="cart-count" hx-swap-oob="true" class="absolute -top-1 -right-1 bg-[var(--clr-gray-00)] text-[var(--clr-secondary-700)] text-xs w-5 h-5 flex items-center justify-center rounded-full">
            {len(cart)}
        </span>
        
        <span id="total-price" hx-swap-oob="true">
            Rs. {format_decimal(total_price, format="#,##,##0.00", locale="ne_NP")}
        </span>
        
        <span class="text-[var(--clr-gray-600)]" id="cart-items-inner" hx-swap-oob="true">({len(cart)})</span>
        """

        context.update({
            "cart": cart,
            "total_price": total_price,
        })

        template_string = render_to_string(self.template_name, context, request=request)
        final_html = template_string + extra_update_html

        return HttpResponse(final_html)
