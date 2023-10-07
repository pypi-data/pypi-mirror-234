from kfsd.apps.endpoints.views.common.model import ModelViewSet


class CustomModelViewSet(ModelViewSet):
    lookup_field = "identifier"
    lookup_value_regex = "[^/]+"
