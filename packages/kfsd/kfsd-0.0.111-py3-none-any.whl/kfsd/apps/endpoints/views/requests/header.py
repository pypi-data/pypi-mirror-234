from drf_spectacular.utils import extend_schema_view

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.requests.header import Header
from kfsd.apps.endpoints.serializers.requests.header import (
    HeaderViewModelSerializer,
)
from kfsd.apps.endpoints.views.requests.docs.header import HeaderDoc


@extend_schema_view(**HeaderDoc.modelviewset())
class HeaderModelViewSet(CustomModelViewSet):
    queryset = Header.objects.all()
    serializer_class = HeaderViewModelSerializer
