from apps.users.forms import UserLoginForm

from .models import Page


def pages_links(request):
    pages = Page.objects.all()
    return {"pages": pages}


def login_form(request):
    form = UserLoginForm(request.POST or None)
    return {"form": form}
