from rest_framework import serializers
from kfsd.apps.endpoints.serializers.base import BaseInputReqSerializer, BaseOutputRespSerializer


class ConfigurationInputReqSerializer(BaseInputReqSerializer):
    op = serializers.ChoiceField(choices=["CONFIG"])


class ConfigurationOutputRespSerializer(BaseOutputRespSerializer):
    op = serializers.ChoiceField(choices=["CONFIG"])
