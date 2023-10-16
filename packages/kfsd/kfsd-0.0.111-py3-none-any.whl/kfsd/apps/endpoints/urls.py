from django.urls import path, include
from rest_framework import routers

from kfsd.apps.endpoints.views.utils.utils import UtilsViewSet
from kfsd.apps.endpoints.views.utils.dump import DumpViewSet

router = routers.DefaultRouter()
router.include_format_suffixes = False

router.register("utils", UtilsViewSet, basename="utils")
router.register("dumps", DumpViewSet, basename="dumps")

urlpatterns = [
    path("", include(router.urls)),
    path("", include("kfsd.apps.endpoints.collection.settings")),
    path("", include("kfsd.apps.endpoints.collection.signals")),
    path("", include("kfsd.apps.endpoints.collection.general")),
    path("", include("kfsd.apps.endpoints.collection.rabbitmq")),
    path("", include("kfsd.apps.endpoints.collection.schema")),
    path("", include("kfsd.apps.endpoints.collection.requests")),
]
