import pika
import pika.exceptions
from kfsd.apps.core.common.logger import Logger, LogLevel
from kfsd.apps.core.common.kubefacets_config import KubefacetsConfig
from kfsd.apps.core.utils.http.django.config import DjangoConfig
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.common.singleton import Singleton
from kfsd.apps.models.tables.rabbitmq.exchange import Exchange
from kfsd.apps.models.tables.rabbitmq.queue import Queue
import json

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class RabbitMQ:
    PROPERTIES = "properties"
    BODY = "body"
    ON_MESSAGE_CALLBACK = "on_message_callback"

    def __init__(self):
        self.__config = DjangoConfig(KubefacetsConfig().getConfig())
        if self.isMQMQEnabled():
            self.prerun()

    @classmethod
    @Singleton
    def getSingleton(cls):
        return cls()

    def isConnectionOpen(self):
        return self.__connection.is_open

    def prerun(self):
        self.establishConnection()
        self.createChannel()
        self.declareExchanges()

    def establishConnection(self):
        self.__connection = self.connect()

    def createChannel(self):
        self.__channel = self.__connection.channel()

    def closeChannel(self):
        self.__channel.close()

    def getConfig(self):
        return self.__config

    def reconnect(self):
        logger.info("Reconnecting RabbitMQ..")
        self.establishConnection()
        self.createChannel()

    def isMQMQEnabled(self):
        return DictUtils.get_by_path(
            self.__config.getConfig(), "services.features_enabled.rabbitmq"
        )

    def connect(self):
        connectionConfig = self.__config.findConfigs(["services.rabbitmq.connect"])[
            0
        ].copy()
        authCredentials = connectionConfig.pop("credentials")
        connectionConfig["credentials"] = self.constructCredentials(
            DictUtils.get(authCredentials, "username"),
            DictUtils.get(authCredentials, "pwd"),
        )
        connection_params = pika.ConnectionParameters(**connectionConfig)
        return pika.BlockingConnection(connection_params)

    def constructCredentials(self, username, pwd):
        return pika.PlainCredentials(username, pwd)

    def declareExchanges(self):
        exchanges = Exchange.objects.all()
        for exchange in exchanges:
            exchangeAttrs = DictUtils.merge(
                dict1={"exchange": exchange.name}, dict2=exchange.attrs
            )
            self.__channel.exchange_declare(**exchangeAttrs)

    def declareQueues(self):
        queues = [queue for queue in Queue.objects.all() if queue.is_declare is True]
        for queue in queues:
            queueAttrs = DictUtils.merge(
                dict1={"queue": queue.name}, dict2=queue.declare_attrs
            )
            self.__channel.queue_declare(**queueAttrs)

    def bindQueues(self):
        queues = [queue for queue in Queue.objects.all() if queue.is_consume is True]
        for queue in queues:
            routes = queue.routes.all()
            for route in routes:
                bindAttrs = {
                    "exchange": route.exchange.name,
                    "routing_key": route.routing_key,
                    "queue": queue.name,
                }
                self.__channel.queue_bind(**bindAttrs)

    def consumeQueues(self, callback):
        self.declareQueues()
        self.bindQueues()
        queues = [queue for queue in Queue.objects.all() if queue.is_consume is True]
        for queue in queues:
            queueAttrs = DictUtils.merge(
                dict1={"queue": queue.name}, dict2=queue.consume_attrs
            )
            self.consume(queueAttrs, callback)

    def publish(self, attrs, msg):
        if not self.isConnectionOpen():
            self.reconnect()
        msg = json.dumps(msg)
        attrs[self.BODY] = msg
        properties = DictUtils.get(attrs, self.PROPERTIES, None)
        if properties:
            properties = pika.BasicProperties(**properties)
            attrs[self.PROPERTIES] = properties
        self.__channel.basic_publish(**attrs)

    def consume(self, attrs, callback):
        attrs[self.ON_MESSAGE_CALLBACK] = callback
        self.__channel.basic_consume(**attrs)

    def closeConnection(self):
        logger.info("Closing RabbitMQ connection!")
        self.__connection.close()

    def startConsuming(self):
        self.__channel.start_consuming()


def close_rabbitmq_connection(self):
    try:
        self.closeConnection()
    except Exception as e:
        logger.error("Could not close RabbitMQ connection!: {}".format(e))
