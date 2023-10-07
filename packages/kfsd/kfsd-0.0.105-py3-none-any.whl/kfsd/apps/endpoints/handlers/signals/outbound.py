from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.signals.outbound import OutboundModelSerializer
from kfsd.apps.models.tables.signals.outbound import Outbound


class OutboundHandler(BaseHandler):
    def __init__(self, outboundIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=OutboundModelSerializer,
            modelClass=Outbound,
            identifier=outboundIdentifier,
            isDBFetch=isDBFetch,
        )
