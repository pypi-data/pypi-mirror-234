from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.signals.docs.v1.outbound import OutboundV1Doc
from kfsd.apps.endpoints.serializers.signals.outbound import OutboundViewModelSerializer
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class OutboundDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**OutboundDoc.modelviewset_list()),
            "retrieve": extend_schema(**OutboundDoc.modelviewset_get()),
            "destroy": extend_schema(**OutboundDoc.modelviewset_delete()),
            "partial_update": extend_schema(**OutboundDoc.modelviewset_patch()),
            "create": extend_schema(**OutboundDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "Outbound - Patch",
            "description": "Outbound Patch",
            "tags": ["MODELS : SIGNALS : OUTBOUND"],
            "responses": {
                200: OutboundViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": OutboundV1Doc.modelviewset_patch_path_examples(),
            "examples": OutboundV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "Outbound - List",
            "description": "Outbound - All",
            "tags": ["MODELS : SIGNALS : OUTBOUND"],
            "responses": {
                200: OutboundViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": OutboundV1Doc.modelviewset_list_path_examples(),
            "examples": OutboundV1Doc.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "Outbound - Get",
            "description": "Outbound Detail",
            "tags": ["MODELS : SIGNALS : OUTBOUND"],
            "responses": {
                200: OutboundViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": OutboundV1Doc.modelviewset_get_path_examples(),
            "examples": OutboundV1Doc.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "Outbound - Create",
            "description": "Outbound - Create",
            "tags": ["MODELS : SIGNALS : OUTBOUND"],
            "responses": {
                200: OutboundViewModelSerializer,
                400: ErrorSerializer,
                404: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": OutboundV1Doc.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "Outbound - Delete",
            "description": "Outbound Delete",
            "tags": ["MODELS : SIGNALS : OUTBOUND"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": OutboundV1Doc.modelviewset_delete_path_examples(),
        }
