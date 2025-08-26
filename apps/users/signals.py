from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from apps.users.constants import UserTypeEnum
from django.contrib.auth.models import Group


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
    elif instance.is_staff and not instance.is_superuser:
        staff_group = Group.objects.get(name="Staffs")
        instance.groups.add(staff_group)