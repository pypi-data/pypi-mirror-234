from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.settings.remote import Remote
from kfsd.apps.endpoints.serializers.settings.remote import RemoteViewModelSerializer
from kfsd.apps.endpoints.views.settings.docs.remote import RemoteDoc
from kfsd.apps.endpoints.handlers.settings.remote import RemoteHandler
from kfsd.apps.endpoints.serializers.settings.local import (
    DimensionsInputReqSerializer,
)
from kfsd.apps.endpoints.serializers.base import parse_request_data


@extend_schema_view(**RemoteDoc.modelviewset())
class RemoteModelViewSet(CustomModelViewSet):
    queryset = Remote.objects.all()
    serializer_class = RemoteViewModelSerializer

    def getDimensionsInputData(self, request):
        return parse_request_data(request, DimensionsInputReqSerializer)

    @extend_schema(**RemoteDoc.exec_view())
    @action(detail=True, methods=["post"])
    def exec(self, request, identifier=None):
        remoteHandler = RemoteHandler(identifier, True)
        return Response(remoteHandler.genConfig(self.getDimensionsInputData(request)))
