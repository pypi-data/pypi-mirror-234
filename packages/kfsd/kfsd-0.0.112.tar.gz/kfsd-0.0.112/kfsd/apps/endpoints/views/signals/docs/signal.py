from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.signals.docs.v1.signal import SignalV1Doc
from kfsd.apps.endpoints.serializers.signals.signal import SignalViewModelSerializer
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
    SuccessSerializer,
)


class SignalDoc:
    @staticmethod
    def exec_view():
        return {
            "summary": "Signal - Exec",
            "description": "Signal Exec",
            "tags": ["MODELS : SIGNALS : SIGNAL"],
            "responses": {
                200: SuccessSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": SignalV1Doc.exec_view_path_examples(),
            "examples": SignalV1Doc.exec_view_examples(),
        }

    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**SignalDoc.modelviewset_list()),
            "retrieve": extend_schema(**SignalDoc.modelviewset_get()),
            "destroy": extend_schema(**SignalDoc.modelviewset_delete()),
            "partial_update": extend_schema(**SignalDoc.modelviewset_patch()),
            "create": extend_schema(**SignalDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "Signal - Patch",
            "description": "Signal Patch",
            "tags": ["MODELS : SIGNALS : SIGNAL"],
            "responses": {
                200: SignalViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": SignalV1Doc.modelviewset_patch_path_examples(),
            "examples": SignalV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "Signal - List",
            "description": "Signal - All",
            "tags": ["MODELS : SIGNALS : SIGNAL"],
            "responses": {
                200: SignalViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": SignalV1Doc.modelviewset_list_path_examples(),
            "examples": SignalV1Doc.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "Signal - Get",
            "description": "Signal Detail",
            "tags": ["MODELS : SIGNALS : SIGNAL"],
            "responses": {
                200: SignalViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": SignalV1Doc.modelviewset_get_path_examples(),
            "examples": SignalV1Doc.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "Signal - Create",
            "description": "Signal - Create",
            "tags": ["MODELS : SIGNALS : SIGNAL"],
            "responses": {
                200: SignalViewModelSerializer,
                400: ErrorSerializer,
                404: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": SignalV1Doc.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "Signal - Delete",
            "description": "Signal Delete",
            "tags": ["MODELS : SIGNALS : SIGNAL"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": SignalV1Doc.modelviewset_delete_path_examples(),
        }
