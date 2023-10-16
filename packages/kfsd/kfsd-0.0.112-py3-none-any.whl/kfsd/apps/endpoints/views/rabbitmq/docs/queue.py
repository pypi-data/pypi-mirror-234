from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.rabbitmq.docs.v1.queue import QueueV1Doc
from kfsd.apps.endpoints.serializers.rabbitmq.queue import QueueViewModelSerializer
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class QueueDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**QueueDoc.modelviewset_list()),
            "retrieve": extend_schema(**QueueDoc.modelviewset_get()),
            "destroy": extend_schema(**QueueDoc.modelviewset_delete()),
            "partial_update": extend_schema(**QueueDoc.modelviewset_patch()),
            "create": extend_schema(**QueueDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "Queue - Patch",
            "description": "Queue Patch",
            "tags": ["MODELS : RABBITMQ : QUEUE"],
            "responses": {
                200: QueueViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": QueueV1Doc.modelviewset_patch_path_examples(),
            "examples": QueueV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "Queue - List",
            "description": "Queue - All",
            "tags": ["MODELS : RABBITMQ : QUEUE"],
            "responses": {
                200: QueueViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": QueueV1Doc.modelviewset_list_path_examples(),
            "examples": QueueV1Doc.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "Queue - Get",
            "description": "Queue Detail",
            "tags": ["MODELS : RABBITMQ : QUEUE"],
            "responses": {
                200: QueueViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": QueueV1Doc.modelviewset_get_path_examples(),
            "examples": QueueV1Doc.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "Queue - Create",
            "description": "Queue - Create",
            "tags": ["MODELS : RABBITMQ : QUEUE"],
            "responses": {
                200: QueueViewModelSerializer,
                400: ErrorSerializer,
                404: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": QueueV1Doc.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "Queue - Delete",
            "description": "Queue Delete",
            "tags": ["MODELS : RABBITMQ : QUEUE"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": QueueV1Doc.modelviewset_delete_path_examples(),
        }
