from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.general.docs.v1.media import MediaV1Doc
from kfsd.apps.endpoints.serializers.general.media import MediaViewModelSerializer
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class MediaDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**MediaDoc.modelviewset_list()),
            "retrieve": extend_schema(**MediaDoc.modelviewset_get()),
            "destroy": extend_schema(**MediaDoc.modelviewset_delete()),
            "partial_update": extend_schema(**MediaDoc.modelviewset_patch()),
            "create": extend_schema(**MediaDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "Media - Patch",
            "description": "Media Patch",
            "tags": ["MODELS : GENERAL : MEDIA"],
            "responses": {
                200: MediaViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": MediaV1Doc.modelviewset_patch_path_examples(),
            "examples": MediaV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "Media - List",
            "description": "Media - All",
            "tags": ["MODELS : GENERAL : MEDIA"],
            "responses": {
                200: MediaViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": MediaV1Doc.modelviewset_list_path_examples(),
            "examples": MediaV1Doc.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "Media - Get",
            "description": "Media Detail",
            "tags": ["MODELS : GENERAL : MEDIA"],
            "responses": {
                200: MediaViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": MediaV1Doc.modelviewset_get_path_examples(),
            "examples": MediaV1Doc.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "Media - Create",
            "description": "Media - Create",
            "tags": ["MODELS : GENERAL : MEDIA"],
            "responses": {
                200: MediaViewModelSerializer,
                400: ErrorSerializer,
                404: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": MediaV1Doc.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "Media - Delete",
            "description": "Media Delete",
            "tags": ["MODELS : GENERAL : MEDIA"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": MediaV1Doc.modelviewset_delete_path_examples(),
        }
