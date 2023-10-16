from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiTypes

from kfsd.apps.endpoints.views.settings.docs.v1.setting import SettingV1Doc
from kfsd.apps.endpoints.serializers.settings.setting import SettingViewModelSerializer
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class SettingDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**SettingDoc.modelviewset_list()),
            "retrieve": extend_schema(**SettingDoc.modelviewset_get()),
            "destroy": extend_schema(**SettingDoc.modelviewset_delete()),
            "partial_update": extend_schema(**SettingDoc.modelviewset_patch()),
            "create": extend_schema(**SettingDoc.modelviewset_create()),
        }

    @staticmethod
    def exec_view():
        return {
            "summary": "Setting - Exec",
            "description": "Setting Exec",
            "tags": ["MODELS : SETTINGS : SETTING"],
            "responses": {
                200: OpenApiTypes.ANY,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": SettingV1Doc.exec_view_path_examples(),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "Setting - Patch",
            "description": "Setting Patch",
            "tags": ["MODELS : SETTINGS : SETTING"],
            "responses": {
                200: SettingViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": SettingV1Doc.modelviewset_patch_path_examples(),
            "examples": SettingV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "Setting - List",
            "description": "Setting - All",
            "tags": ["MODELS : SETTINGS : SETTING"],
            "responses": {
                200: SettingViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": SettingV1Doc.modelviewset_list_path_examples(),
            "examples": SettingV1Doc.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "Setting - Get",
            "description": "Setting Detail",
            "tags": ["MODELS : SETTINGS : SETTING"],
            "responses": {
                200: SettingViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": SettingV1Doc.modelviewset_get_path_examples(),
            "examples": SettingV1Doc.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "Setting - Create",
            "description": "Setting - Create",
            "tags": ["MODELS : SETTINGS : SETTING"],
            "responses": {
                200: SettingViewModelSerializer,
                400: ErrorSerializer,
                404: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": SettingV1Doc.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "Setting - Delete",
            "description": "Setting Delete",
            "tags": ["MODELS : SETTINGS : SETTING"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": SettingV1Doc.modelviewset_delete_path_examples(),
        }
