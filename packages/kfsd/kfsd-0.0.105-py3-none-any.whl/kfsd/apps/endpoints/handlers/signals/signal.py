from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.signals.signal import SignalModelSerializer
from kfsd.apps.models.tables.signals.signal import Signal
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.endpoints.handlers.rabbitmq.producer import ProducerHandler
from kfsd.apps.endpoints.handlers.signals.webhook import WebhookHandler


class SignalHandler(BaseHandler):
    def __init__(self, signalIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=SignalModelSerializer,
            modelClass=Signal,
            identifier=signalIdentifier,
            isDBFetch=isDBFetch,
        )

    def getName(self):
        return DictUtils.get(self.getModelQSData(), "name")

    def getProducers(self):
        return DictUtils.get(self.getModelQSData(), "producers")

    def getWebhooks(self):
        return DictUtils.get(self.getModelQSData(), "webhooks")

    def getDeliveryMethod(self):
        return DictUtils.get(self.getModelQSData(), "delivery")

    def isRetain(self):
        return DictUtils.get(self.getModelQSData(), "is_retain")

    def sendMsgToProducer(self, producerId, msg):
        producerHandler = ProducerHandler(producerId, True)
        producerHandler.exec(msg)

    def sendMsgToWebhook(self, webhookId, msg):
        webhookHandler = WebhookHandler(webhookId, True)
        webhookHandler.exec(msg)

    def sendToAllProducers(self, msg):
        producers = self.getProducers()
        for producer in producers:
            producerId = producer["identifier"]
            self.sendMsgToProducer(producerId, msg)

    def sendToAllWebhooks(self, msg):
        webhooks = self.getWebhooks()
        for webhook in webhooks:
            webhookId = webhook["identifier"]
            self.sendMsgToWebhook(webhookId, msg)

    def exec(self, msg):
        deliveryMethod = self.getDeliveryMethod()
        if deliveryMethod == "MSMQ":
            self.sendToAllProducers(msg)
        elif deliveryMethod == "WEBHOOK":
            self.sendToAllWebhooks(msg)
        elif deliveryMethod == "ALL":
            self.sendToAllProducers(msg)
            self.sendToAllWebhooks(msg)
        return {"detail": "success"}
