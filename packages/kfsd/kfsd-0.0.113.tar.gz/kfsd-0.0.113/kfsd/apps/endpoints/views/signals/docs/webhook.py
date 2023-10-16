from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.signals.docs.v1.webhook import WebhookV1Doc
from kfsd.apps.endpoints.serializers.signals.webhook import WebhookViewModelSerializer
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class WebhookDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**WebhookDoc.modelviewset_list()),
            "retrieve": extend_schema(**WebhookDoc.modelviewset_get()),
            "destroy": extend_schema(**WebhookDoc.modelviewset_delete()),
            "partial_update": extend_schema(**WebhookDoc.modelviewset_patch()),
            "create": extend_schema(**WebhookDoc.modelviewset_create()),
        }

    @staticmethod
    def exec_view():
        return {
            "summary": "Webhook - Exec",
            "description": "Webhook Exec",
            "tags": ["MODELS : SIGNALS : WEBHOOK"],
            "responses": {
                200: WebhookViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": WebhookV1Doc.exec_view_path_examples(),
            "examples": WebhookV1Doc.exec_view_examples(),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "Webhook - Patch",
            "description": "Webhook Patch",
            "tags": ["MODELS : SIGNALS : WEBHOOK"],
            "responses": {
                200: WebhookViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": WebhookV1Doc.modelviewset_patch_path_examples(),
            "examples": WebhookV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "Webhook - List",
            "description": "Webhook - All",
            "tags": ["MODELS : SIGNALS : WEBHOOK"],
            "responses": {
                200: WebhookViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": WebhookV1Doc.modelviewset_list_path_examples(),
            "examples": WebhookV1Doc.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "Webhook - Get",
            "description": "Webhook Detail",
            "tags": ["MODELS : SIGNALS : WEBHOOK"],
            "responses": {
                200: WebhookViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": WebhookV1Doc.modelviewset_get_path_examples(),
            "examples": WebhookV1Doc.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "Webhook - Create",
            "description": "Webhook - Create",
            "tags": ["MODELS : SIGNALS : WEBHOOK"],
            "responses": {
                200: WebhookViewModelSerializer,
                400: ErrorSerializer,
                404: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": WebhookV1Doc.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "Webhook - Delete",
            "description": "Webhook Delete",
            "tags": ["MODELS : SIGNALS : WEBHOOK"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": WebhookV1Doc.modelviewset_delete_path_examples(),
        }
