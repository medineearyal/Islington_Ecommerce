from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("success/", views.SuccessView.as_view(), name="success"),
    path("manual-pay/<str:uuid>/", views.ManualPayQrView.as_view(), name="manual-pay"),
]
