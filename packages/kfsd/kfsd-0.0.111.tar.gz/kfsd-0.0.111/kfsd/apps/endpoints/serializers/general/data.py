from rest_framework import serializers
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
)

from kfsd.apps.models.constants import (
    MAX_LENGTH,
    MIN_LENGTH,
    HTML,
    JSON,
    PLAIN,
    RAW,
    FILE,
)
from kfsd.apps.endpoints.serializers.model import BaseModelSerializer
from kfsd.apps.models.tables.general.data import Data
from kfsd.apps.models.tables.general.file import File
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
    content_type = serializers.ChoiceField(choices=[JSON, HTML, PLAIN])
    source_type = serializers.ChoiceField(choices=[RAW, FILE])
    raw_json_body = serializers.JSONField(default=dict)
    raw_body = serializers.CharField(
        required=False,
        validators=[
            MinLengthValidator(MIN_LENGTH),
        ],
    )
    file = serializers.SlugRelatedField(
        required=False,
        many=False,
        read_only=False,
        slug_field="identifier",
        queryset=File.objects.all(),
    )

    def validate(self, data):
        contentType = get_serializer_val(self, data, "content_type")
        sourceType = get_serializer_val(self, data, "source_type")
        if sourceType == FILE and not get_serializer_val(self, data, "file"):
            raise serializers.ValidationError(
                "file field need to be set if source_type is 'FILE'"
            )

        if (
            contentType == JSON
            and sourceType == RAW
            and not get_serializer_val(self, data, "raw_json_body")
        ):
            raise serializers.ValidationError(
                "raw_json_body field need to be set if content_type is 'JSON'"
            )
        elif (
            contentType in [HTML, PLAIN]
            and sourceType == RAW
            and not get_serializer_val(self, data, "raw_body")
        ):
            raise serializers.ValidationError(
                "raw_body field need to be set if content_type is 'JSON' or 'HTML'"
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
