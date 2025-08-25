from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from apps.common.mixins import SlugMixin
from apps.common.models import TimeStampedModel
from apps.products.models import Tag

# Create your models here.
User = get_user_model()

class BlogCategory(SlugMixin, models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Blog(SlugMixin, TimeStampedModel, models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.BooleanField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="blogs/", null=True, blank=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name="blog_category", null=True, blank=True)
    views = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name
