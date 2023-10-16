from drf_spectacular.utils import extend_schema_view

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.general.media import Media
from kfsd.apps.endpoints.serializers.general.media import MediaViewModelSerializer
from kfsd.apps.endpoints.views.general.docs.media import MediaDoc


@extend_schema_view(**MediaDoc.modelviewset())
class MediaModelViewSet(CustomModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaViewModelSerializer
