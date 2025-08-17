from apps.users.forms import UserLoginForm
from apps.products.models import Category

def header_context(request):
    form = UserLoginForm()
    categories = Category.objects.filter(level=0)

    return {
        "header_categories": categories,
        "header_form": form
    }
