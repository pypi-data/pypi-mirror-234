from rest_framework import generics, status
from rest_framework.views import Response

from kfsd.apps.endpoints.renderers.kubefacetsjson import KubefacetsJSONRenderer
from kfsd.apps.endpoints.views.common.paginate import ModelPagination


class SerializerEvalView(generics.GenericAPIView):
    renderer_classes = [KubefacetsJSONRenderer]
    pagination_class = ModelPagination

    def processRequest(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            validated_data["request"] = request
            return serializer.eval(validated_data)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        return self.processRequest(request)
