from rest_framework import serializers
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
)

from kfsd.apps.endpoints.serializers.model import BaseModelSerializer
from kfsd.apps.models.tables.rabbitmq.exchange import Exchange
from kfsd.apps.models.tables.rabbitmq.route import Route
from kfsd.apps.models.constants import MAX_LENGTH, MIN_LENGTH


class RouteModelSerializer(BaseModelSerializer):
    exchange = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field="identifier",
        queryset=Exchange.objects.all(),
    )
    routing_key = serializers.CharField(
        validators=[
            MinLengthValidator(MIN_LENGTH),
            MaxLengthValidator(MAX_LENGTH),
        ],
    )

    class Meta:
        model = Route
        fields = "__all__"


class RouteViewModelSerializer(RouteModelSerializer):
    id = None
    created = None
    updated = None

    class Meta:
        model = Route
        exclude = ("created", "updated", "id")
