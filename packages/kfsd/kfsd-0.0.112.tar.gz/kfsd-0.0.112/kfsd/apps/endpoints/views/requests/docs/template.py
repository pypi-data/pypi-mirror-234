from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.requests.docs.v1.header import HeaderV1Doc
from kfsd.apps.endpoints.serializers.requests.template import (
    RequestTemplateViewModelSerializer,
)
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class RequestTemplateDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**RequestTemplateDoc.modelviewset_list()),
            "retrieve": extend_schema(**RequestTemplateDoc.modelviewset_get()),
            "destroy": extend_schema(**RequestTemplateDoc.modelviewset_delete()),
            "partial_update": extend_schema(**RequestTemplateDoc.modelviewset_patch()),
            "create": extend_schema(**RequestTemplateDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "Template - Patch",
            "description": "Template Patch",
            "tags": ["MODELS : REQUESTS: TEMPLATE"],
            "responses": {
                200: RequestTemplateViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": HeaderV1Doc.modelviewset_patch_path_examples(),
            "examples": HeaderV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "Template - List",
            "description": "Template - All",
            "tags": ["MODELS : REQUESTS: TEMPLATE"],
            "responses": {
                200: RequestTemplateViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": HeaderV1Doc.modelviewset_list_path_examples(),
            "examples": HeaderV1Doc.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "Template - Get",
            "description": "Template Detail",
            "tags": ["MODELS : REQUESTS: TEMPLATE"],
            "responses": {
                200: RequestTemplateViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": HeaderV1Doc.modelviewset_get_path_examples(),
            "examples": HeaderV1Doc.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "Template - Create",
            "description": "Template - Create",
            "tags": ["MODELS : REQUESTS: TEMPLATE"],
            "responses": {
                200: RequestTemplateViewModelSerializer,
                400: ErrorSerializer,
                404: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": HeaderV1Doc.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "Template - Delete",
            "description": "Template Delete",
            "tags": ["MODELS : REQUESTS: TEMPLATE"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": HeaderV1Doc.modelviewset_delete_path_examples(),
        }
