from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from kfsd.apps.models.tables.signals.base import BaseSignal, log_error
from kfsd.apps.core.common.signal import Signal, inbound_signal_callback_map, tbl_event
from kfsd.apps.core.common.logger import Logger, LogLevel
from kfsd.apps.models.constants import SIGNAL_CLEAR_OUTBOUND

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class Outbound(BaseSignal):
    class Meta:
        app_label = "models"
        verbose_name = "Outbound"
        verbose_name_plural = "Outbound"


def add_signal(name, data):
    Outbound.objects.create(name=name, data=data)


def process_signal(instance):
    try:
        isRetain = Signal.process_outbound_signal(instance.name, instance.data)
        if not isRetain:
            instance.delete()
    except Exception as e:
        logger.error("Recd error on emitting outbound signal: {}".format(e.__str__()))
        log_error(instance, e.__str__())


@receiver(post_save, sender=Outbound)
@tbl_event
def process_post_save(sender, instance, created, **kwargs):
    if created:
        process_signal(instance)


@receiver(post_delete, sender=Outbound)
@tbl_event
def process_post_del(sender, instance, **kwargs):
    pass


def clear_outbound(signal, data):
    outboundQS = Outbound.objects.filter(status="E").order_by("created")
    for instance in outboundQS:
        process_signal(instance)


inbound_signal_callback_map[SIGNAL_CLEAR_OUTBOUND] = clear_outbound
