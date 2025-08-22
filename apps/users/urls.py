from apps.users.views import UserDashboardView, UserOrdersView, UserOrderDetailView, UserOrderTrack, \
    UserOrderTrackDetail, UserProfileView, UserSellerProductsView
from django.urls import path

app_name = "users"

urlpatterns = [
    path("dashboard/", UserDashboardView.as_view(), name="dashboard"),
    path("orders/", UserOrdersView.as_view(), name="orders"),
    path("orders/<str:uuid>/", UserOrderDetailView.as_view(), name="order-detail"),
    path("orders-track/", UserOrderTrack.as_view(), name="order-track"),
    path("orders/track/<str:uuid>/", UserOrderTrackDetail.as_view(), name="order-track-detail"),
    path("profile/<int:pk>/", UserProfileView.as_view(), name="profile"),
    path("products/", UserSellerProductsView.as_view(), name="seller_products"),
]