from .models import SiteSetting


def site_setting(request):
    setting = SiteSetting.objects.first()
    return {"site_setting": setting}
