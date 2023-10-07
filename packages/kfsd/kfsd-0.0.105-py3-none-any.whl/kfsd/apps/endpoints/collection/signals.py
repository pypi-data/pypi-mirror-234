from django.urls import path, include
from rest_framework import routers

from kfsd.apps.endpoints.views.signals.signal import SignalModelViewSet
from kfsd.apps.endpoints.views.signals.webhook import WebhookModelViewSet
from kfsd.apps.endpoints.views.signals.inbound import InboundModelViewSet
from kfsd.apps.endpoints.views.signals.outbound import OutboundModelViewSet

router = routers.DefaultRouter()
router.include_format_suffixes = False

router.register("signals/signal", SignalModelViewSet, basename="signal")
router.register("signals/webhook", WebhookModelViewSet, basename="webhook")
router.register("signals/inbound", InboundModelViewSet, basename="inbound")
router.register("signals/outbound", OutboundModelViewSet, basename="outbound")

urlpatterns = [
    path("", include(router.urls)),
]
