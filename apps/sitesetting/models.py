from django.db import models


# Create your models here.
class SiteSetting(models.Model):
    site_title = models.CharField(max_length=200, default="Marketplace")
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to="photos/logos/", blank=True, null=True)
    favicon = models.ImageField(upload_to="photos/favicons/", blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=255, blank=True, null=True)
    location = models.TextField()
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)

    merchant_name = models.CharField(max_length=255, blank=True, null=True)
    merchant_bank_name = models.CharField(max_length=255, blank=True, null=True)
    merchant_bank_account_number = models.CharField(max_length=255, blank=True, null=True)
    merchant_bank_branch_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "Site Setting"

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"
