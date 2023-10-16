from drf_spectacular.utils import extend_schema_view
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from django.http import HttpResponse
from rest_framework.parsers import MultiPartParser

from kfsd.apps.endpoints.views.common.paginate import ModelPagination

from kfsd.apps.endpoints.views.general.docs.file import FileDoc
from kfsd.apps.models.tables.general.file import File
from kfsd.apps.endpoints.serializers.general.file import FileViewModelSerializer
from kfsd.apps.endpoints.handlers.general.file import FileHandler


class ModelViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    pagination_class = ModelPagination
    filter_backends = [filters.OrderingFilter]
    ordering = ["created"]
    lookup_field = "identifier"
    lookup_value_regex = "[^/]+"


@extend_schema_view(**FileDoc.modelviewset())
class FileModelViewSet(ModelViewSet):
    parser_classes = [MultiPartParser]
    queryset = File.objects.all()
    serializer_class = FileViewModelSerializer

    @extend_schema(**FileDoc.file_view())
    @action(detail=True, methods=["get"])
    def view(self, request, identifier=None):
        fileHandler = FileHandler(identifier, True)
        fileContent = fileHandler.getFile()
        response = HttpResponse(
            fileContent, content_type=fileHandler.getRespContentType()
        )
        response["expires"] = fileHandler.getFileExpiryTime()
        return response

    @extend_schema(**FileDoc.file_thumbnail_view())
    @action(detail=True, methods=["get"])
    def thumbnail(self, request, identifier=None):
        fileHandler = FileHandler(identifier, True)
        fileContent = fileHandler.getThumbnail()
        response = HttpResponse(
            fileContent, content_type=fileHandler.getThumbnailMimeType()
        )
        response["expires"] = fileHandler.getFileExpiryTime()
        return response
