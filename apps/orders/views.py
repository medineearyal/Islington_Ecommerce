from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def order(request):
    return HttpResponse("This is Orders Page")


def cart(request):
    context = {}
    return render(request, "cart/cart.html", context)
