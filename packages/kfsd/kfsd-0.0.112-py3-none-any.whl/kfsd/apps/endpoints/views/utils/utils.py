from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, decorators, renderers, response, status

from kfsd.apps.endpoints.views.utils.docs.utils import UtilsDoc
from kfsd.apps.endpoints.handlers.utils.arr import ArrHandler
from kfsd.apps.endpoints.handlers.utils.attr import AttrHandler
from kfsd.apps.endpoints.handlers.utils.system import SystemHandler
from kfsd.apps.endpoints.serializers.utils.arr import ArrUtilsInputReqSerializer
from kfsd.apps.endpoints.serializers.utils.attr import AttrUtilsInputReqSerializer
from kfsd.apps.endpoints.serializers.utils.system import SystemInputReqSerializer
from kfsd.apps.endpoints.serializers.utils.configuration import (
    ConfigurationInputReqSerializer,
)
from kfsd.apps.endpoints.handlers.common.configuration import ConfigurationHandler
from kfsd.apps.endpoints.renderers.kubefacetsjson import KubefacetsJSONRenderer
from kfsd.apps.endpoints.renderers.kubefacetsyaml import KubefacetsYAMLRenderer
from kfsd.apps.endpoints.serializers.base import parse_request_data


class UtilsViewSet(viewsets.ViewSet):
    lookup_field = "identifier"
    lookup_value_regex = "[^/]+"

    def getSystemInputData(self, request):
        return parse_request_data(request, SystemInputReqSerializer)

    def getArrInputData(self, request):
        return parse_request_data(request, ArrUtilsInputReqSerializer)

    def getAttrInputData(self, request):
        return parse_request_data(request, AttrUtilsInputReqSerializer)

    def getConfigurationInputData(self, request):
        return parse_request_data(request, ConfigurationInputReqSerializer)

    @extend_schema(**UtilsDoc.system_view())
    @decorators.action(
        detail=False, methods=["post"], renderer_classes=[renderers.JSONRenderer]
    )
    def system(self, request):
        systemHandler = SystemHandler(self.getSystemInputData(request))
        return response.Response(systemHandler.gen(), status.HTTP_200_OK)

    @extend_schema(**UtilsDoc.arr_view())
    @decorators.action(
        detail=False, methods=["post"], renderer_classes=[renderers.JSONRenderer]
    )
    def arr(self, request):
        arrHandler = ArrHandler(self.getArrInputData(request))
        return response.Response(arrHandler.gen(), status.HTTP_200_OK)

    @extend_schema(**UtilsDoc.attr_view())
    @decorators.action(
        detail=False, methods=["post"], renderer_classes=[renderers.JSONRenderer]
    )
    def attr(self, request):
        attrHandler = AttrHandler(self.getAttrInputData(request))
        return response.Response(attrHandler.gen(), status.HTTP_200_OK)

    @extend_schema(**UtilsDoc.config_view())
    @decorators.action(
        detail=False,
        methods=["post"],
        renderer_classes=[KubefacetsJSONRenderer, KubefacetsYAMLRenderer],
    )
    def config(self, request):
        configHandler = ConfigurationHandler(self.getConfigurationInputData(request))
        return response.Response(configHandler.gen(), status.HTTP_200_OK)

    @extend_schema(**UtilsDoc.status_view())
    @decorators.action(
        detail=False,
        methods=["get"],
        renderer_classes=[KubefacetsJSONRenderer],
    )
    def status(self, request):
        return response.Response(
            {"detail": "status_ok", "code": 200}, status.HTTP_200_OK
        )
