from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import renderers

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.general.data import Data
from kfsd.apps.endpoints.serializers.general.data import DataViewModelSerializer
from kfsd.apps.endpoints.views.general.docs.data import DataDoc
from kfsd.apps.endpoints.handlers.general.data import DataHandler


@extend_schema_view(**DataDoc.modelviewset())
class DataModelViewSet(CustomModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataViewModelSerializer

    @extend_schema(**DataDoc.body_view())
    @action(
        detail=True,
        methods=["post"],
        renderer_classes=[renderers.JSONRenderer, renderers.StaticHTMLRenderer],
    )
    def body(self, request, identifier=None):
        dataHandler = DataHandler(identifier, True)
        return Response(dataHandler.genBody(request.data))
