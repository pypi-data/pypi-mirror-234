from drf_spectacular.utils import extend_schema_view

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.general.source import Source
from kfsd.apps.endpoints.serializers.general.source import SourceViewModelSerializer
from kfsd.apps.endpoints.views.general.docs.source import SourceDoc


@extend_schema_view(**SourceDoc.modelviewset())
class SourceModelViewSet(CustomModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceViewModelSerializer
