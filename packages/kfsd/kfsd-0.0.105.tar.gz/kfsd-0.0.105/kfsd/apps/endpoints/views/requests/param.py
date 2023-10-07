from drf_spectacular.utils import extend_schema_view

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.requests.param import Param
from kfsd.apps.endpoints.serializers.requests.param import (
    ParamViewModelSerializer,
)
from kfsd.apps.endpoints.views.requests.docs.param import ParamDoc


@extend_schema_view(**ParamDoc.modelviewset())
class ParamModelViewSet(CustomModelViewSet):
    queryset = Param.objects.all()
    serializer_class = ParamViewModelSerializer
