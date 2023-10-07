from django.urls import path, include, re_path
from django.views.generic.base import RedirectView

urlpatterns = [
    re_path(
        r"^$", RedirectView.as_view(url="apis/doc/", permanent=False), name="api_doc"
    ),
    path("apis/", include("kfsd.apps.endpoints.urls")),
]
