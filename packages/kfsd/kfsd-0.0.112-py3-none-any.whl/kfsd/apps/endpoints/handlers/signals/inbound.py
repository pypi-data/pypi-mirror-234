from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.signals.inbound import InboundModelSerializer
from kfsd.apps.models.tables.signals.inbound import Inbound


class InboundHandler(BaseHandler):
    def __init__(self, inboundIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=InboundModelSerializer,
            modelClass=Inbound,
            identifier=inboundIdentifier,
            isDBFetch=isDBFetch,
        )
