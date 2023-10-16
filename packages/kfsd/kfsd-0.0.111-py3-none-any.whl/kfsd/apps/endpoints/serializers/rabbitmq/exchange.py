from rest_framework import serializers
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
)

from kfsd.apps.endpoints.serializers.model import BaseModelSerializer
from kfsd.apps.models.tables.rabbitmq.exchange import Exchange
from kfsd.apps.models.constants import MAX_LENGTH, MIN_LENGTH


class ExchangeModelSerializer(BaseModelSerializer):
    name = serializers.CharField(
        validators=[
            MinLengthValidator(MIN_LENGTH),
            MaxLengthValidator(MAX_LENGTH),
        ]
    )
    attrs = serializers.JSONField(default=dict)

    class Meta:
        model = Exchange
        fields = "__all__"


class ExchangeViewModelSerializer(ExchangeModelSerializer):
    id = None
    created = None
    updated = None

    class Meta:
        model = Exchange
        exclude = ("created", "updated", "id")
