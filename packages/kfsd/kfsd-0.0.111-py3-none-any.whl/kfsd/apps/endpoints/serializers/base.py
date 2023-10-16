from rest_framework import serializers


class BaseInputReqSerializer(serializers.Serializer):
    input = serializers.JSONField(default=dict)


class BaseOutputRespSerializer(serializers.Serializer):
    output = serializers.JSONField()


class ErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()
    code = serializers.CharField()


class NotFoundSerializer(serializers.Serializer):
    detail = serializers.CharField()
    code = serializers.CharField()


class SuccessSerializer(serializers.Serializer):
    detail = serializers.CharField()
    code = serializers.CharField()


def parse_request_data(request, serializer, raiseException=True):
    inputSerializer = serializer(data=request.data)
    inputSerializer.is_valid(raise_exception=raiseException)
    return inputSerializer.data


def get_serializer_val(instance, validated_data, field):
    if field in validated_data:
        return validated_data.get(field, None)
    return instance.initial_data.get(field, None)
