from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.settings.remote import RemoteModelSerializer
from kfsd.apps.models.tables.settings.remote import Remote
from kfsd.apps.endpoints.handlers.requests.endpoint import gen_endpoint_handler


class RemoteHandler(BaseHandler):
    DIMENSIONS_KEY = "dimensions"

    def __init__(self, remoteIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=RemoteModelSerializer,
            modelClass=Remote,
            identifier=remoteIdentifier,
            isDBFetch=isDBFetch,
        )

    def getEndpointHandler(self):
        return gen_endpoint_handler(self.getModelQS().endpoint)

    def genConfig(self, dimensions):
        return self.getEndpointHandler().exec({self.DIMENSIONS_KEY: dimensions}).json()
