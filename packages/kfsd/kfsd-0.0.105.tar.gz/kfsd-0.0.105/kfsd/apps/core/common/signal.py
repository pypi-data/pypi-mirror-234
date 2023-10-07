from kfsd.apps.core.utils.system import System
from kfsd.apps.models.constants import ENV_SERVICE_ID, SIGNAL_TBL_UPSERT
from kfsd.apps.endpoints.handlers.signals.signal import SignalHandler
from functools import wraps

inbound_signal_callback_map = {}


def gen_signal_id(name):
    return "SIGNAL={}".format(name)


def getAppName():
    return System.getEnv(ENV_SERVICE_ID)


def derivedTblEventSignal(kwargs):
    tblName = kwargs["sender"].__name__
    serviceId = getAppName()
    op = "CREATE"
    if "created" in kwargs:
        if not kwargs["created"]:
            op = "UPDATE"
    else:
        op = "DELETE"
    return {
        "action": SIGNAL_TBL_UPSERT,
        "data": {"op": op, "service_id": serviceId, "tbl": tblName},
    }


def tbl_event(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        Signal.process_outbound_signal(SIGNAL_TBL_UPSERT, derivedTblEventSignal(kwargs))
        return data

    return wrapper


class Signal:
    @staticmethod
    def process_inbound_signal(signal, msg):
        if signal in inbound_signal_callback_map:
            signalId = gen_signal_id(signal)
            signalHandler = SignalHandler(signalId, True)
            inbound_signal_callback_map[signal](signal, msg)
            return signalHandler.isRetain()
        else:
            raise NotImplementedError(
                "Inbound signal: {} not implemented.".format(signal)
            )

    @staticmethod
    def process_outbound_signal(signal, msg):
        signalId = gen_signal_id(signal)
        signalHandler = SignalHandler(signalId, True)
        signalHandler.exec(msg)
        return signalHandler.isRetain()
