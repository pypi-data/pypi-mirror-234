from drf_spectacular.utils import extend_schema_view

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.rabbitmq.exchange import Exchange
from kfsd.apps.endpoints.serializers.rabbitmq.exchange import (
    ExchangeViewModelSerializer,
)
from kfsd.apps.endpoints.views.rabbitmq.docs.exchange import ExchangeDoc


@extend_schema_view(**ExchangeDoc.modelviewset())
class ExchangeModelViewSet(CustomModelViewSet):
    queryset = Exchange.objects.all()
    serializer_class = ExchangeViewModelSerializer
