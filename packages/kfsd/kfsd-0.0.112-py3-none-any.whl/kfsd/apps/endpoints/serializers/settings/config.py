from rest_framework import serializers
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
)

from kfsd.apps.endpoints.serializers.model import BaseModelSerializer
from kfsd.apps.models.tables.settings.config import Config
from kfsd.apps.models.constants import MAX_LENGTH, MIN_LENGTH


class ConfigModelSerializer(BaseModelSerializer):
    name = serializers.CharField(
        validators=[
            MinLengthValidator(MIN_LENGTH),
            MaxLengthValidator(MAX_LENGTH),
        ]
    )
    version = serializers.CharField(
        validators=[
            MinLengthValidator(MIN_LENGTH),
            MaxLengthValidator(MAX_LENGTH),
        ]
    )
    is_local_config = serializers.BooleanField(default=True)
    lookup_dimension_keys = serializers.JSONField(default=list)

    class Meta:
        model = Config
        fields = "__all__"


class ConfigViewModelSerializer(ConfigModelSerializer):
    id = None
    created = None
    updated = None

    class Meta:
        model = Config
        exclude = ("created", "updated", "id")
