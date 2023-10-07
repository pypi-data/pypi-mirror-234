from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.signals.webhook import WebhookModelSerializer
from kfsd.apps.models.tables.signals.webhook import Webhook
from kfsd.apps.endpoints.handlers.requests.endpoint import gen_endpoint_handler


class WebhookHandler(BaseHandler):
    def __init__(self, webhookIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=WebhookModelSerializer,
            modelClass=Webhook,
            identifier=webhookIdentifier,
            isDBFetch=isDBFetch,
        )

    def getEndpointHandler(self):
        return gen_endpoint_handler(self.getModelQS().endpoint)

    def exec(self, msg):
        resp = self.getEndpointHandler().exec(msg)
        if hasattr(resp, "data"):
            return resp.data
        else:
            return resp.json()
