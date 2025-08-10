from django.shortcuts import get_object_or_404, render

from .models import Blog


# Create your views here.
def blog(request):
    all_blogs = Blog.objects.all()
    return render(request, "blogs/blogs1.html", {"blogs": all_blogs})


def blog_detail(request, id):
    blog = get_object_or_404(Blog, id=id)
    return render(request, "blogs/details1.html", {"blog": blog})
