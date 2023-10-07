from rest_framework import serializers
from django.core.validators import (
    MinLengthValidator,
)

from kfsd.apps.models.constants import MIN_LENGTH
from kfsd.apps.endpoints.serializers.model import BaseModelSerializer
from kfsd.apps.models.tables.general.media import Media
from kfsd.apps.models.tables.general.source import Source


class MediaModelSerializer(BaseModelSerializer):
    link = serializers.CharField(
        validators=[
            MinLengthValidator(MIN_LENGTH),
        ]
    )
    source = serializers.SlugRelatedField(
        required=False,
        many=False,
        read_only=False,
        slug_field="identifier",
        queryset=Source.objects.all(),
    )
    media_id = serializers.CharField(read_only=True)

    class Meta:
        model = Media
        fields = "__all__"


class MediaViewModelSerializer(MediaModelSerializer):
    id = None
    created = None
    updated = None

    class Meta:
        model = Media
        exclude = ("created", "updated", "id")
