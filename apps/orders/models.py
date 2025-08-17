from django.db import models
from django.utils import timezone

from apps.products.models import Category


# Create your models here.
class Order(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    stock = models.IntegerField(default=1)
    status = models.BooleanField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
