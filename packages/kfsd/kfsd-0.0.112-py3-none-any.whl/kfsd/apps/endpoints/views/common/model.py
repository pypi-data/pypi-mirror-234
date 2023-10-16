from rest_framework import viewsets, filters
from kfsd.apps.endpoints.renderers.kubefacetsjson import KubefacetsJSONRenderer
from kfsd.apps.endpoints.views.common.paginate import ModelPagination


class ModelViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    renderer_classes = [KubefacetsJSONRenderer]
    pagination_class = ModelPagination
    filter_backends = [filters.OrderingFilter]
    ordering = ["created"]
