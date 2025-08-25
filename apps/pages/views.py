import requests
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.db.models.functions import Coalesce, Cast
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView
from django.db.models import Q, When, Case, BooleanField, Value, Min, Max, Avg, Count
from apps.blogs.models import Blog
from apps.products.models import Product, ProductBanner, Category, BestDeals
from django.urls import reverse, reverse_lazy
from .models import Page
from ..orders.constants import PaymentOptions
from ..orders.forms import OrderForm
from ..orders.models import Transaction, KhaltiTransaction
from ..orders.utils import process_cart_totals
from ..products.constans import ShopSortChoicesEnum


# Create your views here.
class HomePageView(TemplateView):
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)

        banners = ProductBanner.objects.filter(is_display=True)[:3]
        categories = Category.objects.annotate(product_count=Count("product_category", distinct=True)).filter(parent__isnull=True, product_count__gt=0)
        best_deals = BestDeals.objects.filter(is_active=True).prefetch_related(
            Prefetch("products", queryset=Product.objects.order_by("-discount"))
        )

        products = Product.objects.all()
        new_arrivals = products.order_by("-created")[:6]

        blogs = Blog.objects.all()[:3]
        pages = Page.objects.all()[:3]

        context.update(
            {
                "banners": banners,
                "categories": categories,
                "best_deals": best_deals.first(),
                "new_arrivals": new_arrivals,

                "products": products,
                "blogs": blogs,
                "pages": pages,
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

        products = Product.objects.all().prefetch_related("reviews")
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

        total_sum, vat_amount, dst_amount = process_cart_totals(cart)

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

        total_sum, vat_amount, dst_amount = process_cart_totals(cart)

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
            order.products = json.dumps(cart)
            order.save()

            request.session["cart"] = {}

            transaction = Transaction.objects.create(
                order=order,
            )

            if payment_method == PaymentOptions.QR:
                return redirect(reverse_lazy("orders:manual-pay", kwargs={"uuid":order.uuid}))
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

                print(response)

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