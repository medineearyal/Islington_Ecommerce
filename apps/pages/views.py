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

        context.update({
            "categories": Category.objects.filter(parent__isnull=True),
            "brands": Category.objects.filter(level=1),
        })

        return context


def page(request):
    all_pages = Page.objects.all()
    return render(request, "pages/page_details.html", {"pages": all_pages})


def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug)
    return render(request, "pages/page_details.html", {"page": page})
