from drf_spectacular.utils import extend_schema, OpenApiTypes

from kfsd.apps.endpoints.views.general.docs.v1.data import DataV1Doc
from kfsd.apps.endpoints.serializers.general.data import (
    DataViewModelSerializer,
)
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class DataDoc:
    @staticmethod
    def body_view():
        return {
            "summary": "Data - Body",
            "description": "Data Body",
            "tags": ["MODELS : GENERAL : DATA"],
            "responses": {
                200: OpenApiTypes.ANY,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": DataV1Doc.body_view_path_examples(),
            "examples": DataV1Doc.body_view_examples(),
        }

    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**DataDoc.modelviewset_list()),
            "retrieve": extend_schema(**DataDoc.modelviewset_get()),
            "destroy": extend_schema(**DataDoc.modelviewset_delete()),
            "partial_update": extend_schema(**DataDoc.modelviewset_patch()),
            "create": extend_schema(**DataDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "Data - Patch",
            "description": "Data Patch",
            "tags": ["MODELS : GENERAL : DATA"],
            "responses": {
                200: DataViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": DataV1Doc.modelviewset_patch_path_examples(),
            "examples": DataV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "Data - List",
            "description": "Data - All",
            "tags": ["MODELS : GENERAL : DATA"],
            "responses": {
                200: DataViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": DataV1Doc.modelviewset_list_path_examples(),
            "examples": DataV1Doc.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "Data - Get",
            "description": "Data Detail",
            "tags": ["MODELS : GENERAL : DATA"],
            "responses": {
                200: DataViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": DataV1Doc.modelviewset_get_path_examples(),
            "examples": DataV1Doc.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "Data - Create",
            "description": "Data - Create",
            "tags": ["MODELS : GENERAL : DATA"],
            "responses": {
                200: DataViewModelSerializer,
                400: ErrorSerializer,
                404: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": DataV1Doc.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "Data - Delete",
            "description": "Data Delete",
            "tags": ["MODELS : GENERAL : DATA"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": DataV1Doc.modelviewset_delete_path_examples(),
        }
