from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import renderers

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.rabbitmq.producer import Producer
from kfsd.apps.endpoints.serializers.rabbitmq.producer import (
    ProducerViewModelSerializer,
)
from kfsd.apps.endpoints.views.rabbitmq.docs.producer import ProducerDoc
from kfsd.apps.endpoints.handlers.rabbitmq.producer import ProducerHandler


@extend_schema_view(**ProducerDoc.modelviewset())
class ProducerModelViewSet(CustomModelViewSet):
    queryset = Producer.objects.all()
    serializer_class = ProducerViewModelSerializer

    @extend_schema(**ProducerDoc.exec_view())
    @action(detail=True, methods=["post"], renderer_classes=[renderers.JSONRenderer])
    def exec(self, request, identifier=None):
        producerHandler = ProducerHandler(identifier, True)
        return Response(producerHandler.exec(request.data))
