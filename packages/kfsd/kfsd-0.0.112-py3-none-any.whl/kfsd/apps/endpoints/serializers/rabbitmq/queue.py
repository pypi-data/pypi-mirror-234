from rest_framework import serializers
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
)

from kfsd.apps.endpoints.serializers.model import BaseModelSerializer
from kfsd.apps.models.tables.rabbitmq.queue import Queue
from kfsd.apps.models.tables.rabbitmq.route import Route
from kfsd.apps.models.constants import MAX_LENGTH, MIN_LENGTH


class QueueModelSerializer(BaseModelSerializer):
    name = serializers.CharField(
        validators=[
            MinLengthValidator(MIN_LENGTH),
            MaxLengthValidator(MAX_LENGTH),
        ],
    )
    is_declare = serializers.BooleanField(default=False)
    is_consume = serializers.BooleanField(default=False)
    declare_attrs = serializers.JSONField(default=dict)
    consume_attrs = serializers.JSONField(default=dict)
    routes = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        slug_field="identifier",
        queryset=Route.objects.all(),
    )

    class Meta:
        model = Queue
        fields = "__all__"


class QueueViewModelSerializer(QueueModelSerializer):
    id = None
    created = None
    updated = None

    class Meta:
        model = Queue
        exclude = ("created", "updated", "id")
