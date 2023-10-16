from rest_framework import generics
from rest_framework.views import Response


class GetAPIView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)
