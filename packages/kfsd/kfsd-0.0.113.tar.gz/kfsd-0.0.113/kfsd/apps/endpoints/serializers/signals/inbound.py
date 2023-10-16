from kfsd.apps.endpoints.serializers.signals.base import BaseSignalModelSerializer
from kfsd.apps.models.tables.signals.inbound import Inbound


class InboundModelSerializer(BaseSignalModelSerializer):
    class Meta:
        model = Inbound
        fields = "__all__"


class InboundViewModelSerializer(InboundModelSerializer):
    id = None
    created = None
    updated = None

    class Meta:
        model = Inbound
        exclude = ("created", "updated", "id")
