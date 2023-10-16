from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.rabbitmq.route import RouteModelSerializer
from kfsd.apps.models.tables.rabbitmq.route import Route


class RouteHandler(BaseHandler):
    def __init__(self, routeIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=RouteModelSerializer,
            modelClass=Route,
            identifier=routeIdentifier,
            isDBFetch=isDBFetch,
        )
