from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.general.docs.v1.group import GroupV1Doc
from kfsd.apps.endpoints.serializers.general.group import (
    GroupViewModelSerializer,
)
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class GroupDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**GroupDoc.modelviewset_list()),
            "retrieve": extend_schema(**GroupDoc.modelviewset_get()),
            "destroy": extend_schema(**GroupDoc.modelviewset_delete()),
            "partial_update": extend_schema(**GroupDoc.modelviewset_patch()),
            "create": extend_schema(**GroupDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "Group - Patch",
            "description": "Group Patch",
            "tags": ["MODELS : GENERAL : GROUP"],
            "responses": {
                200: GroupViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": GroupV1Doc.modelviewset_patch_path_examples(),
            "examples": GroupV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "Group - List",
            "description": "Group - All",
            "tags": ["MODELS : GENERAL : GROUP"],
            "responses": {
                200: GroupViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": GroupV1Doc.modelviewset_list_path_examples(),
            "examples": GroupV1Doc.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "Group - Get",
            "description": "Group Detail",
            "tags": ["MODELS : GENERAL : GROUP"],
            "responses": {
                200: GroupViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": GroupV1Doc.modelviewset_get_path_examples(),
            "examples": GroupV1Doc.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "Group - Create",
            "description": "Group - Create",
            "tags": ["MODELS : GENERAL : GROUP"],
            "responses": {
                200: GroupViewModelSerializer,
                400: ErrorSerializer,
                404: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": GroupV1Doc.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "Group - Delete",
            "description": "Group Delete",
            "tags": ["MODELS : GENERAL : GROUP"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": GroupV1Doc.modelviewset_delete_path_examples(),
        }
