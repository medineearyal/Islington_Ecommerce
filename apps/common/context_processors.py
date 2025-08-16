from django.urls import reverse_lazy


def breadcrumbs(request):
    path = request.path.strip("/").split("/")

    breadcrumb_list = [
        {
            "name": "Home",
            "url": reverse_lazy("home")
        }
    ]

    url_accumulator = ""
    for segment in path:
        url_accumulator += f"/{segment}"
        breadcrumb_list.append({
            "name": segment.replace("-", " ").title(),
            "url": url_accumulator
        })

    if breadcrumb_list:
        breadcrumb_list[-1]["url"] = None

    return {"breadcrumbs": breadcrumb_list}