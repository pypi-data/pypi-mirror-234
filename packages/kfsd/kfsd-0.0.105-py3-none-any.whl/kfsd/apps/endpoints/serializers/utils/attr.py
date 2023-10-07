from rest_framework import serializers
from kfsd.apps.endpoints.serializers.base import BaseInputReqSerializer, BaseOutputRespSerializer


class AttrUtilsInputReqSerializer(BaseInputReqSerializer):
    op = serializers.ChoiceField(choices=["EXPR"])


class AttrUtilsOutputRespSerializer(BaseOutputRespSerializer):
    op = serializers.ChoiceField(choices=["EXPR"])
