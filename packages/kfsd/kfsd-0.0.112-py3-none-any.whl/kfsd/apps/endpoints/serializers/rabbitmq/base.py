from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    RegexValidator,
)
from kfsd.apps.models.constants import MAX_LENGTH, MIN_LENGTH, MSMQ_NAME_REGEX_CONDITION


class MsgSerializer(serializers.Serializer):
    action = serializers.CharField(
        validators=[
            MinLengthValidator(MIN_LENGTH),
            MaxLengthValidator(MAX_LENGTH),
            RegexValidator(
                MSMQ_NAME_REGEX_CONDITION,
                message=_(
                    "action name has to match {}".format(MSMQ_NAME_REGEX_CONDITION)
                ),
                code="action_invalid_name",
            ),
        ],
        required=True,
    )
    target_model = serializers.CharField(required=False)
    data = serializers.JSONField(default=dict)
