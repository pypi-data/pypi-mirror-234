from django.urls import path, include
from rest_framework import routers

from kfsd.apps.endpoints.views.requests.endpoint import EndpointModelViewSet
from kfsd.apps.endpoints.views.requests.header import HeaderModelViewSet

router = routers.DefaultRouter()
router.include_format_suffixes = False

router.register("requests/endpoint", EndpointModelViewSet, basename="endpoint")
router.register("requests/header", HeaderModelViewSet, basename="header")

urlpatterns = [
    path("", include(router.urls)),
]
