from django.urls import path, include
from rest_framework import routers

from kfsd.apps.endpoints.views.general.media import MediaModelViewSet
from kfsd.apps.endpoints.views.general.source import SourceModelViewSet
from kfsd.apps.endpoints.views.general.reference import ReferenceModelViewSet
from kfsd.apps.endpoints.views.general.group import GroupModelViewSet
from kfsd.apps.endpoints.views.general.data import DataModelViewSet
from kfsd.apps.endpoints.views.general.file import FileModelViewSet

router = routers.DefaultRouter()
router.include_format_suffixes = False

router.register("general/group", GroupModelViewSet, basename="group")
router.register("general/source", SourceModelViewSet, basename="source")
router.register("general/media", MediaModelViewSet, basename="media")
router.register("general/reference", ReferenceModelViewSet, basename="reference")
router.register("general/data", DataModelViewSet, basename="data")
router.register("general/file", FileModelViewSet, basename="file")

urlpatterns = [
    path("", include(router.urls)),
]
