from django.urls import path, include
from rest_framework import routers

from kfsd.apps.endpoints.views.rabbitmq.exchange import ExchangeModelViewSet
from kfsd.apps.endpoints.views.rabbitmq.queue import QueueModelViewSet
from kfsd.apps.endpoints.views.rabbitmq.route import RouteModelViewSet
from kfsd.apps.endpoints.views.rabbitmq.producer import ProducerModelViewSet

router = routers.DefaultRouter()
router.include_format_suffixes = False

router.register("rabbitmq/exchanges", ExchangeModelViewSet, basename="exchange")
router.register("rabbitmq/queues", QueueModelViewSet, basename="queue")
router.register("rabbitmq/routes", RouteModelViewSet, basename="route")
router.register("rabbitmq/producers", ProducerModelViewSet, basename="producer")

urlpatterns = [
    path("", include(router.urls)),
]
