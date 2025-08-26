from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("shop/", views.ShopPageView.as_view(), name="shop"),
    path("cart/", views.CartPageView.as_view(), name="cart"),
    path("checkout/", views.CheckoutPageView.as_view(), name="checkout"),
    path("wishlist/", views.WishlistPageView.as_view(), name="wishlist"),
]