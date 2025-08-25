import requests
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Prefetch, IntegerField
from django.db.models.functions import Coalesce, Cast
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView
from django.db.models import Q, When, Case, BooleanField, Value, Min, Max, Avg, Count, F
from apps.blogs.models import Blog
from apps.products.models import Product, ProductBanner, Category, BestDeals, WishList
from django.urls import reverse, reverse_lazy
from .models import Page
from ..common.models import Notices
from ..orders.constants import PaymentOptions
from ..orders.forms import OrderForm
from ..orders.models import Transaction, KhaltiTransaction
from ..orders.utils import process_cart_totals
from ..products.constans import ShopSortChoicesEnum
from ..users.constants import UserTypeEnum


# Create your views here.
class HomePageView(TemplateView):
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)

        banners = ProductBanner.objects.filter(is_display=True)[:3]
        categories = Category.objects.annotate(product_count=Count("product_category", distinct=True)).filter(parent__isnull=True, product_count__gt=0)

        products = Product.objects.all()

        beast_deal_qs = BestDeals.objects.filter(is_active=True)

        user = self.request.user

        if user.is_authenticated and user.user_type == UserTypeEnum.SELLER:
            products = products.exclude(seller=user)
            product_prefetch = Prefetch(
                "products",
                queryset=Product.objects.exclude(seller=user).order_by("-discount"),
            )
        else:
            product_prefetch = Prefetch(
                "products",
                queryset=Product.objects.order_by("-discount")
            )

        beast_deal_qs = beast_deal_qs.prefetch_related(product_prefetch)

        new_arrivals = products.order_by("-created")[:6]

        blogs = Blog.objects.all()[:3]
        pages = Page.objects.all()[:3]

        notices = Notices.objects.filter(is_active=True).order_by("-created")[:3]

        context.update(
            {
                "banners": banners,
                "categories": categories,
                "best_deals": beast_deal_qs.first(),
                "new_arrivals": new_arrivals,

                "products": products,
                "blogs": blogs,
                "pages": pages,
                "notices": notices,
            }
        )

        return context
    
    def get(self, request, *args, **kwargs):
        query = request.GET.get("query")

        if query:
            return redirect(f"{reverse("pages:shop")}?query={query}")

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class ShopPageView(TemplateView):
    template_name = "pages/shop.html"

    def get_context_data(self, **kwargs):
        context = super(ShopPageView, self).get_context_data(**kwargs)

        data = self.request.GET.copy()

        products = Product.objects.all().prefetch_related("reviews").order_by("-created")
        categories = Category.objects.annotate(products=Count("product_category")).filter(parent__isnull=True, products__gt=0)
        brands = Category.objects.filter(level=1)

        category = data.get("category")
        try:
            min_price = int(data.get("min-price", 0))
            max_price = int(data.get("max-price", 0))
        except ValueError:
            min_price = 0
            max_price = 0

        selected_brands = data.getlist("brand")
        tag = data.get("tag")

        if category and category != "all":
            category_instance = get_object_or_404(Category, slug=category)
            category_instance_children_slugs = category_instance.children.values_list("slug", flat=True)

            products = products.filter(
                Q(category__slug=category) | Q(category__slug__in=category_instance_children_slugs)
            )

            brands = brands.filter(
                parent__slug=category
            )

        if min_price and max_price:
            if min_price > max_price:
                min_price = 0
                max_price = 0
            else:
                products = products.filter(price__gte=min_price, price__lte=max_price)

        if selected_brands:
            products = products.filter(category__slug__in=selected_brands)

        if tag:
            products = products.filter(tags__tags__slug=tag)

        prices = products.aggregate(
            min_price=Min("price") if Min("price") is not None else 0,
            max_price=Max("price") if Max("price") is not None else 0,
        )

        query = data.get("product-query")
        if data.get("query"):
            products = products.filter(name__icontains=data["query"])

        if query:
            products = products.filter(name__icontains=query)

        sort = data.get("sort")
        if sort == ShopSortChoicesEnum.PRICE_ASC:
            products = products.order_by("price")
        elif sort == ShopSortChoicesEnum.PRICE_DESC:
            products = products.order_by("-price")
        elif sort == ShopSortChoicesEnum.AZ:
            products = products.order_by("name")
        elif sort == ShopSortChoicesEnum.ZA:
            products = products.order_by("-name")
        elif sort == ShopSortChoicesEnum.POPULAR:
            products = products.annotate(
                ratings=Coalesce(Avg("reviews__rating"), Value(0.00)),
            ).order_by("-ratings")

        paginator = Paginator(products, 24)
        page_num = self.request.GET.get("page")
        products = paginator.get_page(page_num)

        context.update({
            "categories": categories.annotate(
                is_active=Case(
                    When(slug=category, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField()
                )
            ),
            "brands": brands.annotate(
                is_active=Case(
                    When(slug__in=selected_brands, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField()
                )
            ),
            "products": products,
            "min_price": min_price,
            "max_price": max_price,
            "prices": prices,
            "sort": sort,
            "sort_choices": ShopSortChoicesEnum.choices
        })

        return context


class CartPageView(TemplateView):
    template_name = "pages/shopping_cart.html"

    def get_context_data(self, **kwargs):
        context = super(CartPageView, self).get_context_data(**kwargs)
        cart = self.request.session.get("cart", {})

        total_sum, vat_amount, dst_amount, no_of_sellers = process_cart_totals(cart)

        context.update({
            "cart": cart,
            "sub_total": total_sum,
            "final_sum": total_sum + vat_amount + dst_amount,
            "vat_amount": vat_amount,
            "dst_amount": dst_amount,
        })

        return context


class CheckoutPageView(LoginRequiredMixin, TemplateView):
    template_name = "pages/checkout.html"
    login_url = reverse_lazy("account_login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_form = OrderForm()
        cart = self.request.session.get("cart", {})

        total_sum, vat_amount, dst_amount, no_of_sellers = process_cart_totals(cart)

        if no_of_sellers != 1:
            context.update({
                "multi_seller": True
            })

        context.update({
            "form": order_form,
            "cart": cart,
            "sub_total": total_sum,
            "final_sum": round(total_sum + vat_amount + dst_amount),
            "vat_amount": vat_amount,
            "dst_amount": dst_amount,
        })

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if not context["cart"]:
            return redirect("pages:cart")

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)
        context = self.get_context_data(**kwargs)

        if form.is_valid():
            user = request.user if request.user.is_authenticated else None
            payment_method = form.cleaned_data.get("payment_option")
            order = form.save(commit=False)
            order.customer = user
            cart = context.get("cart")
            order.products = cart
            order.save()

            whens = [
                When(id=pid, then=F("stock") - values["quantity"])
                for pid, values in cart.items()
            ]

            Product.objects.filter(id__in=cart.keys()).update(
                stock=Case(*whens, output_field=IntegerField())
            )

            request.session["cart"] = {}

            transaction = Transaction.objects.create(
                order=order,
            )

            multiple_seller = context.get("multi_seller", False)

            if payment_method == PaymentOptions.QR:
                return redirect(f"{reverse_lazy("orders:manual-pay", kwargs={"uuid": order.uuid})}?multi-seller={multiple_seller}")
            elif payment_method == PaymentOptions.KHALTI:
                messages.success(request, "Your Order Has Been Placed Successfully... Happy Shopping!!")
                url = f"{settings.KHALTI_BASE_URL}epayment/initiate/"
                headers = {
                    "Authorization": f"key {settings.KHALTI_API_KEY}",
                    "Content-Type": "application/json"
                }

                payload = json.dumps({
                    "return_url": f"{settings.WEBSITE_URL}{reverse("orders:success")}?tid={transaction.uuid}",
                    "website_url": f"{settings.WEBSITE_URL}{reverse("pages:home")}",
                    "amount": f"{order.total_amount}",
                    "purchase_order_id": f"{order.uuid}",
                    "purchase_order_name": f"{order}",
                    "customer_info": {
                        "name": f"{str(request.user)}",
                        "email": f"{request.user.email}",
                        "phone": "9800000001"
                    }
                })
                response = requests.post(
                    url=url,
                    headers=headers,
                    data=payload
                ).json()

                pidx = response["pidx"]
                KhaltiTransaction.objects.create(
                    transaction=transaction,
                    pidx=pidx,
                    total_amount=order.total_amount,
                    purchase_order_id=f"{order.uuid}",
                    purchase_order_name=f"{str(order)}",
                )

                return redirect(response["payment_url"])
            else:
                messages.success(request, "Your Order Has Been Placed Successfully... Happy Shopping!!")
                return redirect(f"{reverse_lazy("orders:success")}?tid={transaction.uuid}")
        else:
            print(form.errors)
            context.update({
                "form": form,
            })
            messages.error(request, "Something Went Wrong Please Try Again...")
        return render(request, self.template_name, context=context)

class WishlistPageView(LoginRequiredMixin, TemplateView):
    template_name = "pages/wishlist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        wishlist, created = WishList.objects.get_or_create(user=self.request.user)

        context.update({
            "wishlist": wishlist,
        })

        return context


    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        wishlist = context.get("wishlist")

        data = request.GET.copy()
        action = data.get("action")

        if wishlist:
            product_slug = data.get("product_slug")
            if product_slug:
                product = get_object_or_404(Product, slug=product_slug)

                if action == "add":
                    wishlist.products.add(product)
                    messages.success(self.request, "Product Successfully Added to Wishlist.")
                    return redirect("pages:wishlist")
                elif action == "remove":
                    wishlist.products.remove(product)
                    messages.success(self.request, "Product Successfully Removed From the Wishlist.")
                    return redirect("pages:wishlist")
        else:
            messages.error(self.request, "Something Went Wrong Please Try Again...")

        return self.render_to_response(context)


# Error Views
def error_page(request, status_code, message="Something went wrong"):
    return render(
        request,
        "pages/error.html",
        context={
            "status_code": status_code,
            "message": message
        },
        status=status_code
    )

def custom_404(request, exception):
    return error_page(request, 404, str(exception) or "Something went wrong. It’s look that your requested could not be found. It’s look like the link is broken or the page is removed.")

def custom_500(request):
    return error_page(request, 500, "Internal server error")

def custom_403(request, exception):
    return error_page(request, 403, str(exception) or "Permission denied")

def custom_400(request, exception):
    return error_page(request, 400, str(exception) or "Bad request")