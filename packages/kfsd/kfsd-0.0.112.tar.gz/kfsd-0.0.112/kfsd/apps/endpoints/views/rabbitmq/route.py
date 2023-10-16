from drf_spectacular.utils import extend_schema_view

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.rabbitmq.route import Route
from kfsd.apps.endpoints.serializers.rabbitmq.route import RouteViewModelSerializer
from kfsd.apps.endpoints.views.rabbitmq.docs.route import RouteDoc


@extend_schema_view(**RouteDoc.modelviewset())
class RouteModelViewSet(CustomModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteViewModelSerializer
