from django.urls import path
from drf_spectacular.views import SpectacularAPIView

from kfsd.apps.frontend.views.docs.api import APIDocsView


urlpatterns = [
    path("doc/", APIDocsView.as_view(), name="api_doc"),
    path("schema/", SpectacularAPIView.as_view(), name="schema-api"),
]
