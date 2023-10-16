from drf_spectacular.utils import extend_schema_view

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.requests.template import RequestTemplate
from kfsd.apps.endpoints.serializers.requests.template import (
    RequestTemplateViewModelSerializer,
)
from kfsd.apps.endpoints.views.requests.docs.header import HeaderDoc


@extend_schema_view(**HeaderDoc.modelviewset())
class RequestTemplateModelViewSet(CustomModelViewSet):
    queryset = RequestTemplate.objects.all()
    serializer_class = RequestTemplateViewModelSerializer
