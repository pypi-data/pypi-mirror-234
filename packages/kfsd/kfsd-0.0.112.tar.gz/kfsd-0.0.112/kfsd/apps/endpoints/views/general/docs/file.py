from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiTypes

from kfsd.apps.endpoints.views.general.docs.v1.file import FileDocV1
from kfsd.apps.endpoints.serializers.general.file import FileViewModelSerializer
from kfsd.apps.endpoints.serializers.base import NotFoundSerializer, ErrorSerializer


class FileDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**FileDoc.modelviewset_list()),
            "retrieve": extend_schema(**FileDoc.modelviewset_get()),
            "destroy": extend_schema(**FileDoc.modelviewset_delete()),
            "partial_update": extend_schema(**FileDoc.modelviewset_partial_update()),
            "create": extend_schema(**FileDoc.modelviewset_create()),
        }

    @staticmethod
    def file_thumbnail_view():
        return {
            "summary": "File - Thumbnail View",
            "description": "File Thumbnail View",
            "tags": ["MODELS : GENERAL : FILE"],
            "responses": {
                200: OpenApiTypes.BINARY,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": FileDocV1.file_thumbnail_view_path_examples(),
        }

    @staticmethod
    def file_view():
        return {
            "summary": "File - View",
            "description": "File View",
            "tags": ["MODELS : GENERAL : FILE"],
            "responses": {
                200: OpenApiTypes.BINARY,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": FileDocV1.file_view_path_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "File - Create",
            "description": "File Create",
            "tags": ["MODELS : GENERAL : FILE"],
            "responses": {
                200: FileViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "examples": FileDocV1.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "File - List",
            "description": "All Files",
            "tags": ["MODELS : GENERAL : FILE"],
            "responses": {
                200: FileViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": FileDocV1.modelviewset_list_path_examples(),
            "examples": FileDocV1.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "File - Get",
            "description": "File Detail",
            "tags": ["MODELS : GENERAL : FILE"],
            "responses": {
                200: FileViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": FileDocV1.modelviewset_get_path_examples(),
            "examples": FileDocV1.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "File - Delete",
            "description": "File Delete",
            "tags": ["MODELS : GENERAL : FILE"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": FileDocV1.modelviewset_delete_path_examples(),
        }

    @staticmethod
    def modelviewset_partial_update():
        return {
            "summary": "File - Partial Update",
            "description": "File Partial Update",
            "tags": ["MODELS : GENERAL : FILE"],
            "responses": {
                200: FileViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": FileDocV1.modelviewset_partial_update_path_examples(),
            "examples": FileDocV1.modelviewset_partial_update_examples(),
        }
