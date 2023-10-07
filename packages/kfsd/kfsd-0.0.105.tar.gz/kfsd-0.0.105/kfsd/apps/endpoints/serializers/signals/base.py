from rest_framework import serializers
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
)
from kfsd.apps.models.constants import MAX_LENGTH, MIN_LENGTH
from kfsd.apps.endpoints.serializers.model import BaseModelSerializer


class BaseSignalModelSerializer(BaseModelSerializer):
    name = serializers.CharField(
        validators=[
            MinLengthValidator(MIN_LENGTH),
            MaxLengthValidator(MAX_LENGTH),
        ]
    )
    data = serializers.JSONField(default=dict)
    status = serializers.ChoiceField(
        choices=["PENDING", "IN-PROGRESS", "ERROR", "COMPLETED"], default="IN-PROGRESS"
    )
    attempts = serializers.IntegerField(default=0)
    debug_info = serializers.JSONField(default=dict, read_only=True)
