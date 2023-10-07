from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.rabbitmq.producer import ProducerModelSerializer
from kfsd.apps.models.tables.rabbitmq.producer import Producer
from kfsd.apps.core.msmq.rabbitmq.base import RabbitMQ


def gen_producer_handler(instance):
    handler = ProducerHandler(instance.identifier, False)
    qsData = ProducerModelSerializer(instance=instance)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


class ProducerHandler(BaseHandler):
    def __init__(self, producerIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=ProducerModelSerializer,
            modelClass=Producer,
            identifier=producerIdentifier,
            isDBFetch=isDBFetch,
        )

    @staticmethod
    def getProducers(signal):
        signalId = signal
        return Producer.objects.filter(signal=signalId)

    def genPublishAttrs(self):
        return {
            "exchange": self.getModelQS().route.exchange.name,
            "routing_key": self.getModelQS().route.routing_key,
            "properties": self.getModelQS().properties,
        }

    def exec(self, msg):
        rabbitMQ = RabbitMQ()
        if rabbitMQ.isMQMQEnabled():
            rabbitMQ.publish(self.genPublishAttrs(), msg)
        return {"detail": "success"}
