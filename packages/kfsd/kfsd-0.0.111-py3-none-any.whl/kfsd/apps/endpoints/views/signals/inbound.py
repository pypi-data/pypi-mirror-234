from drf_spectacular.utils import extend_schema_view

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.signals.inbound import Inbound
from kfsd.apps.endpoints.serializers.signals.inbound import InboundViewModelSerializer
from kfsd.apps.endpoints.views.signals.docs.inbound import InboundDoc


@extend_schema_view(**InboundDoc.modelviewset())
class InboundModelViewSet(CustomModelViewSet):
    queryset = Inbound.objects.all()
    serializer_class = InboundViewModelSerializer
