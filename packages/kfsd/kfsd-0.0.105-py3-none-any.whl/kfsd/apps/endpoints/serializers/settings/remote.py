from rest_framework import serializers

from kfsd.apps.endpoints.serializers.model import BaseModelSerializer
from kfsd.apps.models.tables.settings.remote import Remote
from kfsd.apps.models.tables.settings.config import Config
from kfsd.apps.models.tables.requests.endpoint import Endpoint


class RemoteModelSerializer(BaseModelSerializer):
    config = serializers.SlugRelatedField(
        required=True,
        many=False,
        read_only=False,
        slug_field="identifier",
        queryset=Config.objects.all(),
    )

    endpoint = serializers.SlugRelatedField(
        required=True,
        many=False,
        read_only=False,
        slug_field="identifier",
        queryset=Endpoint.objects.all(),
    )

    class Meta:
        model = Remote
        fields = "__all__"


class RemoteViewModelSerializer(RemoteModelSerializer):
    id = None
    created = None
    updated = None

    class Meta:
        model = Remote
        exclude = ("created", "updated", "id")
