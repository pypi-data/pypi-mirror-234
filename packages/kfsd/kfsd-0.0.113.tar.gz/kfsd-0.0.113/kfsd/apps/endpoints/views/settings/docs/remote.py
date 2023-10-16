from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.settings.docs.v1.remote import RemoteV1Doc
from kfsd.apps.endpoints.serializers.settings.remote import RemoteViewModelSerializer
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class RemoteDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**RemoteDoc.modelviewset_list()),
            "retrieve": extend_schema(**RemoteDoc.modelviewset_get()),
            "destroy": extend_schema(**RemoteDoc.modelviewset_delete()),
            "partial_update": extend_schema(**RemoteDoc.modelviewset_patch()),
            "create": extend_schema(**RemoteDoc.modelviewset_create()),
        }

    @staticmethod
    def exec_view():
        return {
            "summary": "Remote - Exec",
            "description": "Remote Exec",
            "tags": ["MODELS : SETTINGS : REMOTE"],
            "responses": {
                200: RemoteViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": RemoteV1Doc.modelviewset_patch_path_examples(),
            "examples": RemoteV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "Remote - Patch",
            "description": "Remote Patch",
            "tags": ["MODELS : SETTINGS : REMOTE"],
            "responses": {
                200: RemoteViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": RemoteV1Doc.modelviewset_patch_path_examples(),
            "examples": RemoteV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "Remote - List",
            "description": "Remote - All",
            "tags": ["MODELS : SETTINGS : REMOTE"],
            "responses": {
                200: RemoteViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": RemoteV1Doc.modelviewset_list_path_examples(),
            "examples": RemoteV1Doc.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "Remote - Get",
            "description": "Remote Detail",
            "tags": ["MODELS : SETTINGS : REMOTE"],
            "responses": {
                200: RemoteViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": RemoteV1Doc.modelviewset_get_path_examples(),
            "examples": RemoteV1Doc.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "Remote - Create",
            "description": "Remote - Create",
            "tags": ["MODELS : SETTINGS : REMOTE"],
            "responses": {
                200: RemoteViewModelSerializer,
                400: ErrorSerializer,
                404: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": RemoteV1Doc.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "Remote - Delete",
            "description": "Remote Delete",
            "tags": ["MODELS : SETTINGS : REMOTE"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": RemoteV1Doc.modelviewset_delete_path_examples(),
        }
