from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils import timezone

from apps.common.utils import send_async_email
from apps.users.constants import UserTypeEnum
from django.contrib.auth.models import Group

from apps.users.models import UserRedeemProfile

User = get_user_model()


@receiver(pre_save, sender=User)
def set_username(sender, instance, **kwargs):
    if not instance.username:
        instance.username = instance.email


@receiver(post_save, sender=User)
def assign_users_to_groups(sender, instance, **kwargs):
    if instance.user_type == UserTypeEnum.SELLER:
        seller_group = Group.objects.get(name="Sellers")
        instance.groups.add(seller_group)
        recipient_emails = User.objects.filter(is_staff=True).values_list("email", flat=True)
        html_content = render_to_string("partials/email/new_seller_signed_up.html", context={
            "date": timezone.now().date(),
            "user": instance,
        })
        send_async_email(recipient_emails, html_content=html_content, subject="A new seller has signed up to the platform")
    elif instance.is_staff and not instance.is_superuser:
        staff_group = Group.objects.get(name="Staffs")
        instance.groups.add(staff_group)


@receiver(post_save, sender=User)
def create_user_redeem_profile(sender, instance, created, **kwargs):
    if created:
        UserRedeemProfile.objects.get_or_create(user=instance)
