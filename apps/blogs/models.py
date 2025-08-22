from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

# Create your models here.
User = get_user_model()

class Blog(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.BooleanField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="blogs/", null=True, blank=True)

    def __str__(self):
        return self.name
