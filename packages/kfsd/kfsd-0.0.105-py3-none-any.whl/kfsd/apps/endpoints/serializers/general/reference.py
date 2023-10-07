from rest_framework import serializers
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
)

from kfsd.apps.models.constants import MAX_LENGTH, MIN_LENGTH
from kfsd.apps.endpoints.serializers.model import BaseModelSerializer
from kfsd.apps.models.tables.general.reference import Reference


class ReferenceModelSerializer(BaseModelSerializer):
    identifier = serializers.CharField(read_only=False)
    type = serializers.CharField(
        validators=[
            MinLengthValidator(MIN_LENGTH),
            MaxLengthValidator(MAX_LENGTH),
        ]
    )
    attrs = serializers.JSONField(default=dict)

    class Meta:
        model = Reference
        fields = "__all__"


class ReferenceViewModelSerializer(ReferenceModelSerializer):
    id = None
    created = None
    updated = None

    class Meta:
        model = Reference
        exclude = ("created", "updated", "id")
