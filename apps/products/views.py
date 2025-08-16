from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
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