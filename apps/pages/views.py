from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView

from apps.blogs.models import Blog
from apps.products.models import Product

from .models import Page


# Create your views here.
class HomePageView(TemplateView):
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)

        products = Product.objects.all()
        blogs = Blog.objects.all()[:3]
        pages = Page.objects.all()[:3]

        context.update(
            {
                "products": products,
                "blogs": blogs,
                "pages": pages,
            }
        )

        return context


def page(request):
    all_pages = Page.objects.all()
    return render(request, "pages/page_details.html", {"pages": all_pages})


def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug)
    return render(request, "pages/page_details.html", {"page": page})
