from rest_framework import serializers
from kfsd.apps.endpoints.serializers.base import BaseInputReqSerializer, BaseOutputRespSerializer


class SystemInputReqSerializer(BaseInputReqSerializer):
    op = serializers.ChoiceField(
        choices=[
            "CHECKSUM", "UUID", "SECRET", "KEY", "ENCRYPT_KEY", "OS_ARCH", "HOST_IP", "NIC", "HOSTNAME", "OS"
        ]
    )


class SystemOutputRespSerializer(BaseOutputRespSerializer):
    op = serializers.ChoiceField(
        choices=[
            "CHECKSUM", "UUID", "SECRET", "KEY", "ENCRYPT_KEY", "OS_ARCH", "HOST_IP", "NIC", "HOSTNAME", "OS"
        ]
    )
