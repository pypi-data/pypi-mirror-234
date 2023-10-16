from rest_framework import serializers

from kfsd.apps.endpoints.serializers.model import BaseModelSerializer
from kfsd.apps.models.tables.settings.local import Local
from kfsd.apps.models.tables.settings.config import Config


class LocalModelSerializer(BaseModelSerializer):
    config = serializers.SlugRelatedField(
        required=True,
        many=False,
        read_only=False,
        slug_field="identifier",
        queryset=Config.objects.all(),
    )

    data = serializers.JSONField(default=list)

    class Meta:
        model = Local
        fields = "__all__"


class LocalViewModelSerializer(LocalModelSerializer):
    id = None
    created = None
    updated = None

    class Meta:
        model = Local
        exclude = ("created", "updated", "id")


class DimensionsInputReqSerializer(serializers.Serializer):
    dimensions = serializers.JSONField(default=list)
