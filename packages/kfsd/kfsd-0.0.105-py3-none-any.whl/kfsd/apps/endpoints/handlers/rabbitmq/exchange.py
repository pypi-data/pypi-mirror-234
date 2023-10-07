from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.rabbitmq.exchange import ExchangeModelSerializer
from kfsd.apps.models.tables.rabbitmq.exchange import Exchange


class ExchangeHandler(BaseHandler):
    def __init__(self, exchangeIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=ExchangeModelSerializer,
            modelClass=Exchange,
            identifier=exchangeIdentifier,
            isDBFetch=isDBFetch,
        )
