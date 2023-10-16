from rest_framework import serializers
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
)

from kfsd.apps.models.constants import MAX_LENGTH, MIN_LENGTH
from kfsd.apps.endpoints.serializers.model import BaseModelSerializer
from kfsd.apps.core.utils.file import FileUtils
from kfsd.apps.models.tables.general.file import File

import os


class FileSerializerField(serializers.FileField):
    def to_representation(self, value):
        if FileUtils.path_exists(value.path):
            data = {
                "url": value.url,
                "size": value.size,
                "extension": os.path.splitext(value.name)[1].lower(),
                "path": value.path,
            }
            return data
        return None


class FileModelSerializer(BaseModelSerializer):
    name = serializers.CharField(read_only=True)
    file = FileSerializerField()
    uniq_id = serializers.CharField(read_only=True)
    is_public = serializers.BooleanField(default=False)
    version = serializers.CharField(
        read_only=False,
        validators=[
            MinLengthValidator(MIN_LENGTH),
            MaxLengthValidator(MAX_LENGTH),
        ],
        required=False,
        default="v1",
    )
    expiry_in_mins = serializers.IntegerField(required=False, default=0)

    class Meta:
        model = File
        fields = "__all__"


class FileViewModelSerializer(FileModelSerializer):
    id = None
    created = None
    updated = None

    class Meta:
        model = File
        exclude = ("created", "updated", "id")
