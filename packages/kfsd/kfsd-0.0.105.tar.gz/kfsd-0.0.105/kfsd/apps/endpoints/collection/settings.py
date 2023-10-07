from django.urls import path, include
from rest_framework import routers

from kfsd.apps.endpoints.views.settings.setting import SettingModelViewSet
from kfsd.apps.endpoints.views.settings.config import ConfigModelViewSet
from kfsd.apps.endpoints.views.settings.local import LocalModelViewSet
from kfsd.apps.endpoints.views.settings.remote import RemoteModelViewSet

router = routers.DefaultRouter()
router.include_format_suffixes = False

router.register("settings/setting", SettingModelViewSet, basename="setting")
router.register("settings/config", ConfigModelViewSet, basename="config")
router.register("settings/local", LocalModelViewSet, basename="local")
router.register("settings/remote", RemoteModelViewSet, basename="remote")

urlpatterns = [
    path("", include(router.urls)),
]
