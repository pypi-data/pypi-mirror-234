from drf_spectacular.utils import extend_schema_view
from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.rabbitmq.queue import Queue
from kfsd.apps.endpoints.serializers.rabbitmq.queue import QueueViewModelSerializer
from kfsd.apps.endpoints.views.rabbitmq.docs.queue import QueueDoc


@extend_schema_view(**QueueDoc.modelviewset())
class QueueModelViewSet(CustomModelViewSet):
    queryset = Queue.objects.all()
    serializer_class = QueueViewModelSerializer
