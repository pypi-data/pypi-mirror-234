from kfsd.apps.endpoints.serializers.signals.base import BaseSignalModelSerializer
from kfsd.apps.models.tables.signals.outbound import Outbound


class OutboundModelSerializer(BaseSignalModelSerializer):
    class Meta:
        model = Outbound
        fields = "__all__"


class OutboundViewModelSerializer(OutboundModelSerializer):
    id = None
    created = None
    updated = None

    class Meta:
        model = Outbound
        exclude = ("created", "updated", "id")
