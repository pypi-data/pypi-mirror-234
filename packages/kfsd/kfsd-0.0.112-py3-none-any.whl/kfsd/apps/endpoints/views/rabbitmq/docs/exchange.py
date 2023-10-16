from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.rabbitmq.docs.v1.exchange import ExchangeV1Doc
from kfsd.apps.endpoints.serializers.rabbitmq.exchange import (
    ExchangeViewModelSerializer,
)
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class ExchangeDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**ExchangeDoc.modelviewset_list()),
            "retrieve": extend_schema(**ExchangeDoc.modelviewset_get()),
            "destroy": extend_schema(**ExchangeDoc.modelviewset_delete()),
            "partial_update": extend_schema(**ExchangeDoc.modelviewset_patch()),
            "create": extend_schema(**ExchangeDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "Exchange - Patch",
            "description": "Exchange Patch",
            "tags": ["MODELS : RABBITMQ : EXCHANGE"],
            "responses": {
                200: ExchangeViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": ExchangeV1Doc.modelviewset_patch_path_examples(),
            "examples": ExchangeV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "Exchange - List",
            "description": "Exchange - All",
            "tags": ["MODELS : RABBITMQ : EXCHANGE"],
            "responses": {
                200: ExchangeViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": ExchangeV1Doc.modelviewset_list_path_examples(),
            "examples": ExchangeV1Doc.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "Exchange - Get",
            "description": "Exchange Detail",
            "tags": ["MODELS : RABBITMQ : EXCHANGE"],
            "responses": {
                200: ExchangeViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": ExchangeV1Doc.modelviewset_get_path_examples(),
            "examples": ExchangeV1Doc.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "Exchange - Create",
            "description": "Exchange - Create",
            "tags": ["MODELS : RABBITMQ : EXCHANGE"],
            "responses": {
                200: ExchangeViewModelSerializer,
                400: ErrorSerializer,
                404: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": ExchangeV1Doc.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "Exchange - Delete",
            "description": "Exchange Delete",
            "tags": ["MODELS : RABBITMQ : EXCHANGE"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": ExchangeV1Doc.modelviewset_delete_path_examples(),
        }
