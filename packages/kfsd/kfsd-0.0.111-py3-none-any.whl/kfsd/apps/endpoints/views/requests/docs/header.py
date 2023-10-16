from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.requests.docs.v1.header import HeaderV1Doc
from kfsd.apps.endpoints.serializers.requests.header import (
    HeaderViewModelSerializer,
)
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class HeaderDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**HeaderDoc.modelviewset_list()),
            "retrieve": extend_schema(**HeaderDoc.modelviewset_get()),
            "destroy": extend_schema(**HeaderDoc.modelviewset_delete()),
            "partial_update": extend_schema(**HeaderDoc.modelviewset_patch()),
            "create": extend_schema(**HeaderDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "Header - Patch",
            "description": "Header Patch",
            "tags": ["MODELS : REQUESTS: HEADER"],
            "responses": {
                200: HeaderViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": HeaderV1Doc.modelviewset_patch_path_examples(),
            "examples": HeaderV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "Header - List",
            "description": "Header - All",
            "tags": ["MODELS : REQUESTS: HEADER"],
            "responses": {
                200: HeaderViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": HeaderV1Doc.modelviewset_list_path_examples(),
            "examples": HeaderV1Doc.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "Header - Get",
            "description": "Header Detail",
            "tags": ["MODELS : REQUESTS: HEADER"],
            "responses": {
                200: HeaderViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": HeaderV1Doc.modelviewset_get_path_examples(),
            "examples": HeaderV1Doc.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "Header - Create",
            "description": "Header - Create",
            "tags": ["MODELS : REQUESTS: HEADER"],
            "responses": {
                200: HeaderViewModelSerializer,
                400: ErrorSerializer,
                404: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": HeaderV1Doc.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "Header - Delete",
            "description": "Header Delete",
            "tags": ["MODELS : REQUESTS: HEADER"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": HeaderV1Doc.modelviewset_delete_path_examples(),
        }
