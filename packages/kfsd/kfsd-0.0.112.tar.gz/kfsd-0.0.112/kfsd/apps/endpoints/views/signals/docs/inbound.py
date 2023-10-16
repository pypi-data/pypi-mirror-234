from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.signals.docs.v1.inbound import InboundV1Doc
from kfsd.apps.endpoints.serializers.signals.inbound import InboundViewModelSerializer
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class InboundDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**InboundDoc.modelviewset_list()),
            "retrieve": extend_schema(**InboundDoc.modelviewset_get()),
            "destroy": extend_schema(**InboundDoc.modelviewset_delete()),
            "partial_update": extend_schema(**InboundDoc.modelviewset_patch()),
            "create": extend_schema(**InboundDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "Inbound - Patch",
            "description": "Inbound Patch",
            "tags": ["MODELS : SIGNALS : INBOUND"],
            "responses": {
                200: InboundViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": InboundV1Doc.modelviewset_patch_path_examples(),
            "examples": InboundV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "Inbound - List",
            "description": "Inbound - All",
            "tags": ["MODELS : SIGNALS : INBOUND"],
            "responses": {
                200: InboundViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": InboundV1Doc.modelviewset_list_path_examples(),
            "examples": InboundV1Doc.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "Inbound - Get",
            "description": "Inbound Detail",
            "tags": ["MODELS : SIGNALS : INBOUND"],
            "responses": {
                200: InboundViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": InboundV1Doc.modelviewset_get_path_examples(),
            "examples": InboundV1Doc.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "Inbound - Create",
            "description": "Inbound - Create",
            "tags": ["MODELS : SIGNALS : INBOUND"],
            "responses": {
                200: InboundViewModelSerializer,
                400: ErrorSerializer,
                404: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": InboundV1Doc.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "Inbound - Delete",
            "description": "Inbound Delete",
            "tags": ["MODELS : SIGNALS : INBOUND"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": InboundV1Doc.modelviewset_delete_path_examples(),
        }
