from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, StaticHTMLRenderer

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.requests.endpoint import Endpoint
from kfsd.apps.endpoints.serializers.requests.endpoint import (
    EndpointViewModelSerializer,
)
from kfsd.apps.endpoints.views.requests.docs.endpoint import EndpointDoc
from kfsd.apps.endpoints.handlers.requests.endpoint import EndpointHandler
import json


@extend_schema_view(**EndpointDoc.modelviewset())
class EndpointModelViewSet(CustomModelViewSet):
    queryset = Endpoint.objects.all()
    serializer_class = EndpointViewModelSerializer

    @extend_schema(**EndpointDoc.exec_view())
    @action(
        detail=True,
        methods=["post"],
        renderer_classes=[JSONRenderer, StaticHTMLRenderer],
    )
    def exec(self, request, identifier=None):
        endpointHandler = EndpointHandler(identifier, True)
        resp = endpointHandler.exec(json.loads(request.body.decode("utf-8")))
        return Response(resp.content)
