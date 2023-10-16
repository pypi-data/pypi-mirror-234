from kfsd.apps.endpoints.serializers.base import ErrorSerializer, SuccessSerializer
from kfsd.apps.endpoints.views.utils.docs.v1.utils import UtilsV1Doc
from kfsd.apps.endpoints.serializers.utils.arr import (
    ArrUtilsInputReqSerializer,
    ArrUtilsOutputRespSerializer,
)
from kfsd.apps.endpoints.serializers.utils.system import (
    SystemInputReqSerializer,
    SystemOutputRespSerializer,
)
from kfsd.apps.endpoints.serializers.utils.attr import (
    AttrUtilsInputReqSerializer,
    AttrUtilsOutputRespSerializer,
)
from kfsd.apps.endpoints.serializers.utils.configuration import (
    ConfigurationInputReqSerializer,
    ConfigurationOutputRespSerializer,
)


class UtilsDoc:
    @staticmethod
    def status_view():
        return {
            "summary": "Status",
            "tags": ["MODELS : COMMON : UTILS"],
            "responses": {200: SuccessSerializer, 500: ErrorSerializer},
            "examples": UtilsV1Doc.status_examples(),
        }

    @staticmethod
    def config_view():
        return {
            "summary": "Config",
            "tags": ["MODELS : COMMON : UTILS"],
            "request": ConfigurationInputReqSerializer,
            "responses": {200: ConfigurationOutputRespSerializer, 500: ErrorSerializer},
            "examples": UtilsV1Doc.config_examples(),
        }

    @staticmethod
    def arr_view():
        return {
            "summary": "Array",
            "tags": ["MODELS : COMMON : UTILS"],
            "request": ArrUtilsInputReqSerializer,
            "responses": {200: ArrUtilsOutputRespSerializer, 500: ErrorSerializer},
            "examples": UtilsV1Doc.arr_examples(),
        }

    @staticmethod
    def system_view():
        return {
            "summary": "System",
            "tags": ["MODELS : COMMON : UTILS"],
            "request": SystemInputReqSerializer,
            "responses": {200: SystemOutputRespSerializer, 500: ErrorSerializer},
            "examples": UtilsV1Doc.system_examples(),
        }

    @staticmethod
    def attr_view():
        return {
            "summary": "Attr",
            "tags": ["MODELS : COMMON : UTILS"],
            "request": AttrUtilsInputReqSerializer,
            "responses": {200: AttrUtilsOutputRespSerializer, 500: ErrorSerializer},
            "examples": UtilsV1Doc.attr_examples(),
        }
