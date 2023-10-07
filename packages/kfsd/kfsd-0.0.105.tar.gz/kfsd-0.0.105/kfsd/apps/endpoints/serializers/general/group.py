from rest_framework import serializers

from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    RegexValidator,
)
from django.utils.translation import gettext_lazy as _

from kfsd.apps.models.constants import MAX_LENGTH, MIN_LENGTH
from kfsd.apps.models.tables.general.group import Group
from kfsd.apps.models.tables.general.media import Media
from kfsd.apps.models.tables.general.reference import Reference
from kfsd.apps.models.constants import GROUP_NAME_REGEX_CONDITION

from kfsd.apps.endpoints.serializers.model import BaseModelSerializer


class GroupModelSerializer(BaseModelSerializer):
    parent = serializers.SlugRelatedField(
        required=False,
        many=False,
        read_only=False,
        slug_field="identifier",
        queryset=Group.objects.all(),
    )
    media = serializers.SlugRelatedField(
        required=False,
        many=True,
        read_only=False,
        slug_field="identifier",
        queryset=Media.objects.all(),
    )
    members = serializers.SlugRelatedField(
        required=False,
        many=True,
        read_only=False,
        slug_field="identifier",
        queryset=Reference.objects.all(),
    )
    groups = serializers.SlugRelatedField(
        required=False,
        many=True,
        read_only=False,
        slug_field="identifier",
        queryset=Group.objects.all(),
    )
    name = serializers.CharField(
        required=True,
        validators=[
            MinLengthValidator(MIN_LENGTH),
            MaxLengthValidator(MAX_LENGTH),
            RegexValidator(
                GROUP_NAME_REGEX_CONDITION,
                message=_(
                    "name didn't match validation, regex: {}".format(
                        GROUP_NAME_REGEX_CONDITION
                    )
                ),
                code="invalid_name",
            ),
        ],
    )
    type = serializers.CharField(
        validators=[MinLengthValidator(MIN_LENGTH), MaxLengthValidator(MAX_LENGTH)],
    )

    class Meta:
        model = Group
        fields = "__all__"


class GroupViewModelSerializer(GroupModelSerializer):
    id = None
    created = None
    updated = None

    class Meta:
        model = Group
        exclude = ("created", "updated", "id")
