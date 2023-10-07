from rest_framework import serializers
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
)

from kfsd.apps.models.constants import MAX_LENGTH, MIN_LENGTH, HTML, JSON, PLAIN
from kfsd.apps.endpoints.serializers.model import BaseModelSerializer
from kfsd.apps.models.tables.general.data import Data
from kfsd.apps.endpoints.serializers.base import get_serializer_val


class DataModelSerializer(BaseModelSerializer):
    name = serializers.CharField(
        validators=[
            MinLengthValidator(MIN_LENGTH),
            MaxLengthValidator(MAX_LENGTH),
        ]
    )
    is_template = serializers.BooleanField(default=False)
    default_template_values = serializers.JSONField(default=dict)
    body = serializers.CharField(
        required=False,
        validators=[
            MinLengthValidator(MIN_LENGTH),
        ],
    )
    content_type = serializers.ChoiceField(choices=[JSON, HTML, PLAIN])
    json_body = serializers.JSONField(default=dict)

    def validate(self, data):
        contentType = get_serializer_val(self, data, "content_type")
        if contentType == JSON and not get_serializer_val(self, data, "json_body"):
            raise serializers.ValidationError(
                "json_body field need to be set if content_type is 'JSON'"
            )
        elif contentType in [HTML, PLAIN] and not get_serializer_val(
            self, data, "body"
        ):
            raise serializers.ValidationError(
                "body field need to be set if content_type is 'JSON' or 'HTML'"
            )

        return data

    class Meta:
        model = Data
        fields = "__all__"


class DataViewModelSerializer(DataModelSerializer):
    id = None
    created = None
    updated = None

    class Meta:
        model = Data
        exclude = ("created", "updated", "id")
