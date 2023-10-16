from drf_spectacular.utils import extend_schema_view

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.signals.outbound import Outbound
from kfsd.apps.endpoints.serializers.signals.outbound import OutboundViewModelSerializer
from kfsd.apps.endpoints.views.signals.docs.outbound import OutboundDoc


@extend_schema_view(**OutboundDoc.modelviewset())
class OutboundModelViewSet(CustomModelViewSet):
    queryset = Outbound.objects.all()
    serializer_class = OutboundViewModelSerializer
