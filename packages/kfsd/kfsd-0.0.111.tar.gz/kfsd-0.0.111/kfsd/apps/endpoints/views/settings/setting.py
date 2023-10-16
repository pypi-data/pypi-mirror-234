from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.settings.setting import Setting
from kfsd.apps.endpoints.serializers.settings.setting import SettingViewModelSerializer
from kfsd.apps.endpoints.views.settings.docs.setting import SettingDoc
from kfsd.apps.endpoints.handlers.settings.setting import SettingHandler


@extend_schema_view(**SettingDoc.modelviewset())
class SettingModelViewSet(CustomModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingViewModelSerializer

    @extend_schema(**SettingDoc.exec_view())
    @action(detail=True, methods=["get"])
    def exec(self, request, identifier=None):
        settingHandler = SettingHandler(identifier, True)
        return Response(settingHandler.genConfig())
