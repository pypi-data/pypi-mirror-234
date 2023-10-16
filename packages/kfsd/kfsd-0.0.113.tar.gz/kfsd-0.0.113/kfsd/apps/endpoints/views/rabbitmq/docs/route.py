from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.rabbitmq.docs.v1.producer import ProducerV1Doc
from kfsd.apps.endpoints.serializers.rabbitmq.producer import (
    ProducerViewModelSerializer,
)
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class RouteDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**RouteDoc.modelviewset_list()),
            "retrieve": extend_schema(**RouteDoc.modelviewset_get()),
            "destroy": extend_schema(**RouteDoc.modelviewset_delete()),
            "partial_update": extend_schema(**RouteDoc.modelviewset_patch()),
            "create": extend_schema(**RouteDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "Route - Patch",
            "description": "Route Patch",
            "tags": ["MODELS : RABBITMQ : ROUTE"],
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
            "summary": "Route - List",
            "description": "Route - All",
            "tags": ["MODELS : RABBITMQ : ROUTE"],
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
            "summary": "Route - Get",
            "description": "Route Detail",
            "tags": ["MODELS : RABBITMQ : ROUTE"],
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
            "summary": "Route - Create",
            "description": "Route - Create",
            "tags": ["MODELS : RABBITMQ : ROUTE"],
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
            "summary": "Route - Delete",
            "description": "Route Delete",
            "tags": ["MODELS : RABBITMQ : ROUTE"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": ProducerV1Doc.modelviewset_delete_path_examples(),
        }
