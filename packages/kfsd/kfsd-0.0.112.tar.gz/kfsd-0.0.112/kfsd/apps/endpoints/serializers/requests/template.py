from rest_framework import serializers

from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
)

from kfsd.apps.models.constants import MAX_LENGTH, MIN_LENGTH

from kfsd.apps.endpoints.serializers.model import BaseModelSerializer
from kfsd.apps.models.tables.requests.header import Header
from kfsd.apps.models.tables.requests.param import Param
from kfsd.apps.models.tables.requests.template import RequestTemplate


class RequestTemplateModelSerializer(BaseModelSerializer):
    name = serializers.CharField(
        required=True,
        validators=[
            MinLengthValidator(MIN_LENGTH),
            MaxLengthValidator(MAX_LENGTH),
        ],
    )
    headers = serializers.SlugRelatedField(
        required=False,
        many=True,
        read_only=False,
        slug_field="identifier",
        queryset=Header.objects.all(),
    )
    params = serializers.SlugRelatedField(
        required=False,
        many=True,
        read_only=False,
        slug_field="identifier",
        queryset=Param.objects.all(),
    )

    class Meta:
        model = RequestTemplate
        fields = "__all__"


class RequestTemplateViewModelSerializer(RequestTemplateModelSerializer):
    id = None
    created = None
    updated = None

    class Meta:
        model = RequestTemplate
        exclude = ("created", "updated", "id")
