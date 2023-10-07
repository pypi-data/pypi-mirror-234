from rest_framework import serializers

from kfsd.apps.endpoints.serializers.model import BaseModelSerializer
from kfsd.apps.models.tables.rabbitmq.route import Route
from kfsd.apps.models.tables.signals.signal import Signal
from kfsd.apps.models.tables.rabbitmq.producer import Producer


class ProducerModelSerializer(BaseModelSerializer):
    signal = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field="identifier",
        queryset=Signal.objects.all(),
    )
    route = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field="identifier",
        queryset=Route.objects.all(),
    )
    properties = serializers.JSONField(default=dict)

    class Meta:
        model = Producer
        fields = "__all__"


class ProducerViewModelSerializer(ProducerModelSerializer):
    id = None
    created = None
    updated = None

    class Meta:
        model = Producer
        exclude = ("created", "updated", "id")
