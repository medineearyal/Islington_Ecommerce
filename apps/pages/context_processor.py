from apps.users.forms import UserLoginForm

from .models import Page
from apps.products.models import Category


def pages_links(request):
    pages = Page.objects.all()
    return {"pages": pages}

def header_context(request):
    form = UserLoginForm()
    categories = Category.objects.filter(level=0)

    return {
        "header_categories": categories,
        "header_form": form
    }
