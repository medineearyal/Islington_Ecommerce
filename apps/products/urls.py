from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "products"

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="shop", permanent=True)),
    path('compare/', views.compare_products, name='compare_products'),
    path('compare/add/<int:product_id>/', views.add_to_compare, name='add_to_compare'),
    path('compare/remove/<int:product_id>/', views.remove_from_compare, name='remove_from_compare'),

    path("<str:slug>/", views.ProductDetailView.as_view(), name="detail"),
    path("cart/<int:pk>/", views.CartView.as_view(), name="cart"),

    path("products/create/", views.product_create, name="create"),
    path("products/edit/<int:pk>/", views.product_edit, name="edit"),
    path("products/cateogry/create/", views.CategoryView.as_view(), name="create_category"),
    path("products/colors/create/", views.ProductColorsView.as_view(), name="create_color"),

    path("products/quick_view/<str:slug>/", views.product_detail_modal, name="quick_view")
]