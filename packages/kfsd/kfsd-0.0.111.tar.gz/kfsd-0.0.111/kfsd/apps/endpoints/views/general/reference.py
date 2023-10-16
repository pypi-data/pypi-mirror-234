from drf_spectacular.utils import extend_schema_view

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.general.reference import Reference
from kfsd.apps.endpoints.serializers.general.reference import (
    ReferenceViewModelSerializer,
)
from kfsd.apps.endpoints.views.general.docs.reference import ReferenceDoc


@extend_schema_view(**ReferenceDoc.modelviewset())
class ReferenceModelViewSet(CustomModelViewSet):
    queryset = Reference.objects.all()
    serializer_class = ReferenceViewModelSerializer
