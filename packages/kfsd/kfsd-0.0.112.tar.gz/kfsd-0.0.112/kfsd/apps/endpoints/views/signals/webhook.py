from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import renderers

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.signals.webhook import Webhook
from kfsd.apps.endpoints.serializers.signals.webhook import WebhookViewModelSerializer
from kfsd.apps.endpoints.views.signals.docs.webhook import WebhookDoc
from kfsd.apps.endpoints.handlers.signals.webhook import WebhookHandler


@extend_schema_view(**WebhookDoc.modelviewset())
class WebhookModelViewSet(CustomModelViewSet):
    queryset = Webhook.objects.all()
    serializer_class = WebhookViewModelSerializer

    @extend_schema(**WebhookDoc.exec_view())
    @action(detail=True, methods=["post"], renderer_classes=[renderers.JSONRenderer])
    def exec(self, request, identifier=None):
        webhookHandler = WebhookHandler(identifier, True)
        return Response(webhookHandler.exec(request.data))
