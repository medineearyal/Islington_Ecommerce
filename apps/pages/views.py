from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.db.models.functions import Coalesce, Cast
from django.forms import DecimalField
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.db.models import Q, When, Case, BooleanField, Value, Min, Max, Avg
from apps.blogs.models import Blog
from apps.products.models import Product, ProductBanner, Category, BestDeals

from .models import Page
from ..products.constans import ShopSortChoicesEnum


# Create your views here.
class HomePageView(TemplateView):
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)

        banners = ProductBanner.objects.filter(is_display=True)[:3]
        categories = Category.objects.filter(parent__isnull=True)
        best_deals = BestDeals.objects.filter(is_active=True).prefetch_related(
            Prefetch("products", queryset=Product.objects.order_by("-discount"))
        ).first()

        products = Product.objects.all()
        blogs = Blog.objects.all()[:3]
        pages = Page.objects.all()[:3]

        context.update(
            {
                "banners": banners,
                "categories": categories,
                "best_deals": best_deals,

                "products": products,
                "blogs": blogs,
                "pages": pages,
            }
        )

        return context


class ShopPageView(TemplateView):
    template_name = "pages/shop.html"

    def get_context_data(self, **kwargs):
        context = super(ShopPageView, self).get_context_data(**kwargs)

        data = self.request.GET.copy()

        products = Product.objects.all().prefetch_related("reviews")
        categories = Category.objects.filter(parent__isnull=True)
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
        if query:
            products.filter(name__icontains=query)

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
