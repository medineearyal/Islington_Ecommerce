from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


# Create your models here.
class Page(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    content = CKEditor5Field()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
