from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.outpost import OutpostModelSerializer
from kfsd.apps.models.tables.outpost import Outpost


class OutpostHandler(BaseHandler):
    def __init__(self, outpostIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=OutpostModelSerializer,
            modelClass=Outpost,
            identifier=outpostIdentifier,
            isDBFetch=isDBFetch,
        )

    def updateStatus(self, status):
        pass
