from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.general.docs.v1.reference import ReferenceV1Doc
from kfsd.apps.endpoints.serializers.general.reference import (
    ReferenceViewModelSerializer,
)
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class ReferenceDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**ReferenceDoc.modelviewset_list()),
            "retrieve": extend_schema(**ReferenceDoc.modelviewset_get()),
            "destroy": extend_schema(**ReferenceDoc.modelviewset_delete()),
            "partial_update": extend_schema(**ReferenceDoc.modelviewset_patch()),
            "create": extend_schema(**ReferenceDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "Reference - Patch",
            "description": "Reference Patch",
            "tags": ["MODELS : GENERAL : REFERENCE"],
            "responses": {
                200: ReferenceViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": ReferenceV1Doc.modelviewset_patch_path_examples(),
            "examples": ReferenceV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "Reference - List",
            "description": "Reference - All",
            "tags": ["MODELS : GENERAL : REFERENCE"],
            "responses": {
                200: ReferenceViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": ReferenceV1Doc.modelviewset_list_path_examples(),
            "examples": ReferenceV1Doc.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "Reference - Get",
            "description": "Reference Detail",
            "tags": ["MODELS : GENERAL : REFERENCE"],
            "responses": {
                200: ReferenceViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": ReferenceV1Doc.modelviewset_get_path_examples(),
            "examples": ReferenceV1Doc.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "Reference - Create",
            "description": "Reference - Create",
            "tags": ["MODELS : GENERAL : REFERENCE"],
            "responses": {
                200: ReferenceViewModelSerializer,
                400: ErrorSerializer,
                404: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": ReferenceV1Doc.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "Reference - Delete",
            "description": "Reference Delete",
            "tags": ["MODELS : GENERAL : REFERENCE"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": ReferenceV1Doc.modelviewset_delete_path_examples(),
        }
