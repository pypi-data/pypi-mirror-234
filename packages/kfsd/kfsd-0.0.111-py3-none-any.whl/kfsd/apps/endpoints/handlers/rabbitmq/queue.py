from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.rabbitmq.queue import QueueModelSerializer
from kfsd.apps.models.tables.rabbitmq.queue import Queue


class QueueHandler(BaseHandler):
    def __init__(self, queueIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=QueueModelSerializer,
            modelClass=Queue,
            identifier=queueIdentifier,
            isDBFetch=isDBFetch,
        )
