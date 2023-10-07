from rest_framework import serializers
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
)

from kfsd.apps.endpoints.serializers.model import BaseModelSerializer
from kfsd.apps.models.tables.settings.setting import Setting
from kfsd.apps.models.tables.settings.config import Config
from kfsd.apps.models.constants import MAX_LENGTH, MIN_LENGTH


class SettingModelSerializer(BaseModelSerializer):
    name = serializers.CharField(
        validators=[
            MinLengthValidator(MIN_LENGTH),
            MaxLengthValidator(MAX_LENGTH),
        ]
    )
    config = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field="identifier",
        queryset=Config.objects.all(),
    )

    class Meta:
        model = Setting
        fields = "__all__"


class SettingViewModelSerializer(SettingModelSerializer):
    id = None
    created = None
    updated = None

    class Meta:
        model = Setting
        exclude = ("created", "updated", "id")
