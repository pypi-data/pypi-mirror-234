from rest_framework import serializers
from kfsd.apps.endpoints.serializers.base import (
    BaseInputReqSerializer,
    BaseOutputRespSerializer,
)


class ArrUtilsInputReqSerializer(BaseInputReqSerializer):
    op = serializers.ChoiceField(choices=["JOIN", "INTERSECTION", "MERGE"])


class ArrUtilsOutputRespSerializer(BaseOutputRespSerializer):
    op = serializers.ChoiceField(choices=["JOIN", "INTERSECTION", "MERGE"])
