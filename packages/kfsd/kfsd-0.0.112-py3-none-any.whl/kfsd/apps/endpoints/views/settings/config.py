from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.settings.config import Config
from kfsd.apps.endpoints.serializers.settings.config import ConfigViewModelSerializer
from kfsd.apps.endpoints.views.settings.docs.config import ConfigDoc
from kfsd.apps.endpoints.handlers.settings.config import ConfigHandler


@extend_schema_view(**ConfigDoc.modelviewset())
class ConfigModelViewSet(CustomModelViewSet):
    queryset = Config.objects.all()
    serializer_class = ConfigViewModelSerializer

    @extend_schema(**ConfigDoc.exec_view())
    @action(detail=True, methods=["get"])
    def exec(self, request, identifier=None):
        configHandler = ConfigHandler(identifier, True)
        return Response(configHandler.genConfig())
