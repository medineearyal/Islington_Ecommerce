from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "products"

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="shop", permanent=True)),
    path("<str:slug>/", views.ProductDetailView.as_view(), name="detail"),
]
