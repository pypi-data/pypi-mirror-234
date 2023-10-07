from rest_framework import serializers

from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
)

from kfsd.apps.models.constants import MAX_LENGTH, MIN_LENGTH

from kfsd.apps.endpoints.serializers.model import BaseModelSerializer
from kfsd.apps.models.tables.requests.header import Header


class HeaderModelSerializer(BaseModelSerializer):
    name = serializers.CharField(
        required=True,
        validators=[
            MinLengthValidator(MIN_LENGTH),
            MaxLengthValidator(MAX_LENGTH),
        ],
    )
    key = serializers.CharField(
        required=True,
        validators=[
            MinLengthValidator(MIN_LENGTH),
            MaxLengthValidator(MAX_LENGTH),
        ],
    )
    value = serializers.CharField(
        required=True,
        validators=[
            MinLengthValidator(MIN_LENGTH),
            MaxLengthValidator(MAX_LENGTH),
        ],
    )

    class Meta:
        model = Header
        fields = "__all__"


class HeaderViewModelSerializer(HeaderModelSerializer):
    id = None
    created = None
    updated = None

    class Meta:
        model = Header
        exclude = ("created", "updated", "id")
