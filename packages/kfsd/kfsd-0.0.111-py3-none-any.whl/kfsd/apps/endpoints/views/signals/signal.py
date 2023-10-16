from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import renderers

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.signals.signal import Signal
from kfsd.apps.endpoints.serializers.signals.signal import SignalViewModelSerializer
from kfsd.apps.endpoints.views.signals.docs.signal import SignalDoc
from kfsd.apps.endpoints.handlers.signals.signal import SignalHandler


@extend_schema_view(**SignalDoc.modelviewset())
class SignalModelViewSet(CustomModelViewSet):
    queryset = Signal.objects.all()
    serializer_class = SignalViewModelSerializer

    @extend_schema(**SignalDoc.exec_view())
    @action(detail=True, methods=["post"], renderer_classes=[renderers.JSONRenderer])
    def exec(self, request, identifier=None):
        signalHandler = SignalHandler(identifier, True)
        return Response(signalHandler.exec(request.data))
