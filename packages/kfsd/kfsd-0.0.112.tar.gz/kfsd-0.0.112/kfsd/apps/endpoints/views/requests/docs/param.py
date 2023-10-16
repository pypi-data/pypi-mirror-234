from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.requests.docs.v1.param import ParamV1Doc
from kfsd.apps.endpoints.serializers.requests.param import (
    ParamViewModelSerializer,
)
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class ParamDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**ParamDoc.modelviewset_list()),
            "retrieve": extend_schema(**ParamDoc.modelviewset_get()),
            "destroy": extend_schema(**ParamDoc.modelviewset_delete()),
            "partial_update": extend_schema(**ParamDoc.modelviewset_patch()),
            "create": extend_schema(**ParamDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "Param - Patch",
            "description": "Param Patch",
            "tags": ["MODELS : REQUESTS: PARAM"],
            "responses": {
                200: ParamViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": ParamV1Doc.modelviewset_patch_path_examples(),
            "examples": ParamV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "Param - List",
            "description": "Param - All",
            "tags": ["MODELS : REQUESTS: PARAM"],
            "responses": {
                200: ParamViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": ParamV1Doc.modelviewset_list_path_examples(),
            "examples": ParamV1Doc.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "Param - Get",
            "description": "Param Detail",
            "tags": ["MODELS : REQUESTS: PARAM"],
            "responses": {
                200: ParamViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": ParamV1Doc.modelviewset_get_path_examples(),
            "examples": ParamV1Doc.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "Param - Create",
            "description": "Param - Create",
            "tags": ["MODELS : REQUESTS: PARAM"],
            "responses": {
                200: ParamViewModelSerializer,
                400: ErrorSerializer,
                404: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": ParamV1Doc.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "Param - Delete",
            "description": "Param Delete",
            "tags": ["MODELS : REQUESTS: PARAM"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": ParamV1Doc.modelviewset_delete_path_examples(),
        }
