from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, DetailView
from django.db.models import Case, When, Value, BooleanField
from .models import Blog, BlogCategory


# Create your views here.
class BlogPageView(TemplateView):
    template_name = "pages/blogs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        blogs = Blog.objects.all().order_by("-created")

        paginator = Paginator(blogs, 10)
        page = self.request.GET.get("page")
        page_obj = paginator.get_page(page)

        categories = BlogCategory.objects.filter()

        data = self.request.GET.copy()
        category_slug = data.get('category')

        if category_slug != "all" and category_slug is not None:
            blogs = blogs.filter(category__slug=data.get("category"))

        query = data.get("blog-query")
        if query:
            blogs = blogs.filter(name__icontains=query)

        context.update({
            "blogs": page_obj,
            "categories": categories.annotate(
                is_active=Case(
                    When(slug=category_slug, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField()
                )
            ),
        })

        return context


class BlogDetailView(DetailView):
    model = Blog
    template_name = "pages/blog_detail.html"
    context_object_name = "blog"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = BlogCategory.objects.filter()
        related_posts = Blog.objects.filter(category=self.object.category).order_by("-created").exclude(pk=self.object.pk)

        context.update({
            "categories": categories,
            "related_posts": related_posts,
        })

        return context