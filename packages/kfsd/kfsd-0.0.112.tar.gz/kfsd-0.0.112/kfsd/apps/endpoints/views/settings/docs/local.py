from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiTypes
from kfsd.apps.endpoints.views.settings.docs.v1.local import LocalV1Doc
from kfsd.apps.endpoints.serializers.settings.local import LocalViewModelSerializer
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class LocalDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**LocalDoc.modelviewset_list()),
            "retrieve": extend_schema(**LocalDoc.modelviewset_get()),
            "destroy": extend_schema(**LocalDoc.modelviewset_delete()),
            "partial_update": extend_schema(**LocalDoc.modelviewset_patch()),
            "create": extend_schema(**LocalDoc.modelviewset_create()),
        }

    @staticmethod
    def exec_view():
        return {
            "summary": "Local - Exec",
            "description": "Local Exec",
            "tags": ["MODELS : SETTINGS : LOCAL"],
            "responses": {
                200: OpenApiTypes.ANY,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": LocalV1Doc.exec_view_path_examples(),
            "examples": LocalV1Doc.exec_view_examples(),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "Local - Patch",
            "description": "Local Patch",
            "tags": ["MODELS : SETTINGS : LOCAL"],
            "responses": {
                200: LocalViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": LocalV1Doc.modelviewset_patch_path_examples(),
            "examples": LocalV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "Local - List",
            "description": "Local - All",
            "tags": ["MODELS : SETTINGS : LOCAL"],
            "responses": {
                200: LocalViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": LocalV1Doc.modelviewset_list_path_examples(),
            "examples": LocalV1Doc.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "Local - Get",
            "description": "Local Detail",
            "tags": ["MODELS : SETTINGS : LOCAL"],
            "responses": {
                200: LocalViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": LocalV1Doc.modelviewset_get_path_examples(),
            "examples": LocalV1Doc.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "Local - Create",
            "description": "Local - Create",
            "tags": ["MODELS : SETTINGS : LOCAL"],
            "responses": {
                200: LocalViewModelSerializer,
                400: ErrorSerializer,
                404: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": LocalV1Doc.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "Local - Delete",
            "description": "Local Delete",
            "tags": ["MODELS : SETTINGS : LOCAL"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": LocalV1Doc.modelviewset_delete_path_examples(),
        }
