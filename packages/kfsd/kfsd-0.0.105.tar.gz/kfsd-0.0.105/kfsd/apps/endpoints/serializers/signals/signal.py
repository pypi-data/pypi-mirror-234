from rest_framework import serializers
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
)
from kfsd.apps.models.constants import MAX_LENGTH, MIN_LENGTH
from kfsd.apps.endpoints.serializers.model import BaseModelSerializer
from kfsd.apps.models.tables.signals.signal import Signal
from kfsd.apps.endpoints.serializers.rabbitmq.producer import (
    ProducerViewModelSerializer,
)
from kfsd.apps.endpoints.serializers.signals.webhook import (
    WebhookViewModelSerializer,
)


class SignalModelSerializer(BaseModelSerializer):
    name = serializers.CharField(
        validators=[
            MinLengthValidator(MIN_LENGTH),
            MaxLengthValidator(MAX_LENGTH),
        ]
    )
    delivery = serializers.ChoiceField(choices=["MSMQ", "WEBHOOK", "ALL", "NONE"])
    is_retain = serializers.BooleanField(default=False)
    producers = ProducerViewModelSerializer(many=True)
    webhooks = WebhookViewModelSerializer(many=True)

    class Meta:
        model = Signal
        fields = "__all__"


class SignalViewModelSerializer(SignalModelSerializer):
    id = None
    created = None
    updated = None

    class Meta:
        model = Signal
        exclude = ("created", "updated", "id")
