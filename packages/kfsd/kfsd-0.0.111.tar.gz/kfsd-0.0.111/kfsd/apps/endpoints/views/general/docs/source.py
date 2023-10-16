from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.general.docs.v1.source import SourceV1Doc
from kfsd.apps.endpoints.serializers.general.source import (
    SourceViewModelSerializer,
)
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class SourceDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**SourceDoc.modelviewset_list()),
            "retrieve": extend_schema(**SourceDoc.modelviewset_get()),
            "destroy": extend_schema(**SourceDoc.modelviewset_delete()),
            "partial_update": extend_schema(**SourceDoc.modelviewset_patch()),
            "create": extend_schema(**SourceDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "Source - Patch",
            "description": "Source Patch",
            "tags": ["MODELS : GENERAL : SOURCE"],
            "responses": {
                200: SourceViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": SourceV1Doc.modelviewset_patch_path_examples(),
            "examples": SourceV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "Source - List",
            "description": "Source - All",
            "tags": ["MODELS : GENERAL : SOURCE"],
            "responses": {
                200: SourceViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": SourceV1Doc.modelviewset_list_path_examples(),
            "examples": SourceV1Doc.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "Source - Get",
            "description": "Source Detail",
            "tags": ["MODELS : GENERAL : SOURCE"],
            "responses": {
                200: SourceViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": SourceV1Doc.modelviewset_get_path_examples(),
            "examples": SourceV1Doc.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "Source - Create",
            "description": "Source - Create",
            "tags": ["MODELS : GENERAL : SOURCE"],
            "responses": {
                200: SourceViewModelSerializer,
                400: ErrorSerializer,
                404: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": SourceV1Doc.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "Source - Delete",
            "description": "Source Delete",
            "tags": ["MODELS : GENERAL : SOURCE"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": SourceV1Doc.modelviewset_delete_path_examples(),
        }
