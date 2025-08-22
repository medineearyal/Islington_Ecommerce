from .models import SiteSetting


def site_setting(request):
    setting = SiteSetting.objects.first()
    return {"setting": setting}
