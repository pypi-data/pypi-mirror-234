from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiTypes

from kfsd.apps.endpoints.views.requests.docs.v1.endpoint import EndpointV1Doc
from kfsd.apps.endpoints.serializers.requests.endpoint import (
    EndpointViewModelSerializer,
)
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class EndpointDoc:
    @staticmethod
    def exec_view():
        return {
            "summary": "Endpoint - Exec",
            "description": "Endpoint Exec",
            "tags": ["MODELS : REQUESTS: ENDPOINT"],
            "responses": {
                200: OpenApiTypes.ANY,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": EndpointV1Doc.exec_view_path_examples(),
            "examples": EndpointV1Doc.exec_view_examples(),
        }

    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**EndpointDoc.modelviewset_list()),
            "retrieve": extend_schema(**EndpointDoc.modelviewset_get()),
            "destroy": extend_schema(**EndpointDoc.modelviewset_delete()),
            "partial_update": extend_schema(**EndpointDoc.modelviewset_patch()),
            "create": extend_schema(**EndpointDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "Endpoint - Patch",
            "description": "Endpoint Patch",
            "tags": ["MODELS : REQUESTS: ENDPOINT"],
            "responses": {
                200: EndpointViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": EndpointV1Doc.modelviewset_patch_path_examples(),
            "examples": EndpointV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "Endpoint - List",
            "description": "Endpoint - All",
            "tags": ["MODELS : REQUESTS: ENDPOINT"],
            "responses": {
                200: EndpointViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": EndpointV1Doc.modelviewset_list_path_examples(),
            "examples": EndpointV1Doc.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "Endpoint - Get",
            "description": "Endpoint Detail",
            "tags": ["MODELS : REQUESTS: ENDPOINT"],
            "responses": {
                200: EndpointViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": EndpointV1Doc.modelviewset_get_path_examples(),
            "examples": EndpointV1Doc.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "Endpoint - Create",
            "description": "Endpoint - Create",
            "tags": ["MODELS : REQUESTS: ENDPOINT"],
            "responses": {
                200: EndpointViewModelSerializer,
                400: ErrorSerializer,
                404: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": EndpointV1Doc.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "Endpoint - Delete",
            "description": "Endpoint Delete",
            "tags": ["MODELS : REQUESTS: ENDPOINT"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": EndpointV1Doc.modelviewset_delete_path_examples(),
        }
