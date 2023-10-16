from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.rabbitmq.docs.v1.producer import ProducerV1Doc
from kfsd.apps.endpoints.serializers.rabbitmq.producer import (
    ProducerViewModelSerializer,
)
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
    SuccessSerializer,
)


class ProducerDoc:
    @staticmethod
    def exec_view():
        return {
            "summary": "Producer - Exec",
            "description": "Producer Exec",
            "tags": ["MODELS : RABBITMQ : PRODUCER"],
            "responses": {
                200: SuccessSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": ProducerV1Doc.exec_view_path_examples(),
            "examples": ProducerV1Doc.exec_view_examples(),
        }

    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**ProducerDoc.modelviewset_list()),
            "retrieve": extend_schema(**ProducerDoc.modelviewset_get()),
            "destroy": extend_schema(**ProducerDoc.modelviewset_delete()),
            "partial_update": extend_schema(**ProducerDoc.modelviewset_patch()),
            "create": extend_schema(**ProducerDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "Producer - Patch",
            "description": "Producer Patch",
            "tags": ["MODELS : RABBITMQ : PRODUCER"],
            "responses": {
                200: ProducerViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": ProducerV1Doc.modelviewset_patch_path_examples(),
            "examples": ProducerV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "Producer - List",
            "description": "Producer - All",
            "tags": ["MODELS : RABBITMQ : PRODUCER"],
            "responses": {
                200: ProducerViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": ProducerV1Doc.modelviewset_list_path_examples(),
            "examples": ProducerV1Doc.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "Producer - Get",
            "description": "Producer Detail",
            "tags": ["MODELS : RABBITMQ : PRODUCER"],
            "responses": {
                200: ProducerViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": ProducerV1Doc.modelviewset_get_path_examples(),
            "examples": ProducerV1Doc.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "Producer - Create",
            "description": "Producer - Create",
            "tags": ["MODELS : RABBITMQ : PRODUCER"],
            "responses": {
                200: ProducerViewModelSerializer,
                400: ErrorSerializer,
                404: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": ProducerV1Doc.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "Producer - Delete",
            "description": "Producer Delete",
            "tags": ["MODELS : RABBITMQ : PRODUCER"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": ProducerV1Doc.modelviewset_delete_path_examples(),
        }
