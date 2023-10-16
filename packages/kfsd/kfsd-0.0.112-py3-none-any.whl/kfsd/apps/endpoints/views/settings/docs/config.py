from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.settings.docs.v1.config import ConfigV1Doc
from kfsd.apps.endpoints.serializers.settings.config import ConfigViewModelSerializer
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class ConfigDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**ConfigDoc.modelviewset_list()),
            "retrieve": extend_schema(**ConfigDoc.modelviewset_get()),
            "destroy": extend_schema(**ConfigDoc.modelviewset_delete()),
            "partial_update": extend_schema(**ConfigDoc.modelviewset_patch()),
            "create": extend_schema(**ConfigDoc.modelviewset_create()),
        }

    @staticmethod
    def exec_view():
        return {
            "summary": "Config - Exec",
            "description": "Config Exec",
            "tags": ["MODELS : SETTINGS : CONFIG"],
            "responses": {
                200: ConfigViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": ConfigV1Doc.modelviewset_patch_path_examples(),
            "examples": ConfigV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "Config - Patch",
            "description": "Config Patch",
            "tags": ["MODELS : SETTINGS : CONFIG"],
            "responses": {
                200: ConfigViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": ConfigV1Doc.modelviewset_patch_path_examples(),
            "examples": ConfigV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "Config - List",
            "description": "Config - All",
            "tags": ["MODELS : SETTINGS : CONFIG"],
            "responses": {
                200: ConfigViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": ConfigV1Doc.modelviewset_list_path_examples(),
            "examples": ConfigV1Doc.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "Config - Get",
            "description": "Config Detail",
            "tags": ["MODELS : SETTINGS : CONFIG"],
            "responses": {
                200: ConfigViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": ConfigV1Doc.modelviewset_get_path_examples(),
            "examples": ConfigV1Doc.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "Config - Create",
            "description": "Config - Create",
            "tags": ["MODELS : SETTINGS : CONFIG"],
            "responses": {
                200: ConfigViewModelSerializer,
                400: ErrorSerializer,
                404: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": ConfigV1Doc.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "Config - Delete",
            "description": "Config Delete",
            "tags": ["MODELS : SETTINGS : CONFIG"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": ConfigV1Doc.modelviewset_delete_path_examples(),
        }
