from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.settings.local import Local
from kfsd.apps.endpoints.serializers.settings.local import (
    LocalViewModelSerializer,
    DimensionsInputReqSerializer,
)
from kfsd.apps.endpoints.views.settings.docs.local import LocalDoc
from kfsd.apps.endpoints.handlers.settings.local import LocalHandler


@extend_schema_view(**LocalDoc.modelviewset())
class LocalModelViewSet(CustomModelViewSet):
    queryset = Local.objects.all()
    serializer_class = LocalViewModelSerializer

    def parseInput(self, request, serializer):
        inputSerializer = serializer(data=request.data)
        inputSerializer.is_valid()
        return inputSerializer.data

    def getDimensionsInputData(self, request):
        return self.parseInput(request, DimensionsInputReqSerializer)

    @extend_schema(**LocalDoc.exec_view())
    @action(detail=True, methods=["post"])
    def exec(self, request, identifier=None):
        localHandler = LocalHandler(identifier, True)
        return Response(
            localHandler.genConfig(self.getDimensionsInputData(request)["dimensions"])
        )
