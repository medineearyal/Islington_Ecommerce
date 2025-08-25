from django.urls import path

from . import views

app_name = 'blogs'

urlpatterns = [
    path("", views.BlogPageView.as_view(), name="blogs"),
    path("<slug:slug>/", views.BlogDetailView.as_view(), name="blog_detail"),
]
