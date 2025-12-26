from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"
    
    def ready(self):
        import apps.users.signals #noqa

        try:
            from django.contrib.auth.models import Group, Permission
            from django.contrib.contenttypes.models import ContentType
            from allauth.account.models import EmailAddress
            from apps.users.models import AuthUser
            from apps.sitesetting.models import SiteSetting

            seller, created = Group.objects.get_or_create(name="Sellers")
            perms = [
                Permission.objects.get(codename="add_product"),
                Permission.objects.get(codename="change_product")
            ]

            if not created:
                seller.permissions.set(perms)

            staffs, created = Group.objects.get_or_create(name="Staffs")
            email_address = ContentType.objects.get_for_model(EmailAddress)
            groups_ct = ContentType.objects.get_for_model(Group)
            users_ct = ContentType.objects.get_for_model(AuthUser)
            site_setting_ct = ContentType.objects.get_for_model(SiteSetting)


            perms = Permission.objects.exclude(content_type__in=[email_address, groups_ct, users_ct, site_setting_ct])

            staffs.permissions.set(perms)
        except Exception:
            pass
