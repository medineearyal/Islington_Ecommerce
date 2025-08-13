from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView

from apps.blogs.models import Blog
from apps.products.models import Product, ProductBanner, Category, BestDeals

from .models import Page


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
        products = Product.objects.all()

        category = data.get("category")
        min_price = data.get("min")
        max_price = data.get("max")
        brand = data.get("brand")
        tag = data.get("tag")

        if category:
            products = products.filter(category__slug=category)

        if min_price and max_price:
            products = products.filter(price__gte=min_price, price__lte=max_price)
        elif min_price:
            products = products.filter(price__gte=min_price)
        elif max_price:
            products = products.filter(price_lte=max_price)

        if brand:
            products = products.filter(category__slug=brand)

        if tag:
            products = products.filter(tags__tags__slug=tag)



        context.update({
            "categories": Category.objects.filter(parent__isnull=True),
            "brands": Category.objects.filter(level=1),
            "products": products,
        })

        return context
