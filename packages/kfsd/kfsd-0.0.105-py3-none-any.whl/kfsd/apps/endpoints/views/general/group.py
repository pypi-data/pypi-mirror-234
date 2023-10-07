from drf_spectacular.utils import extend_schema_view

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.general.group import Group
from kfsd.apps.endpoints.serializers.general.group import GroupViewModelSerializer
from kfsd.apps.endpoints.views.general.docs.group import GroupDoc


@extend_schema_view(**GroupDoc.modelviewset())
class GroupModelViewSet(CustomModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupViewModelSerializer
