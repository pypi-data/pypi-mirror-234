from datetime import datetime, timedelta, date
from django.utils import timezone
import time

from kfsd.apps.core.exceptions.exec import ExecExceptionHandler
from kfsd.apps.core.common.logger import Logger, LogLevel

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class Time:
    @staticmethod
    @ExecExceptionHandler(logger)
    def current_date():
        today = date.today()
        return today.strftime("%Y-%m-%d")

    @staticmethod
    @ExecExceptionHandler(logger)
    def sleep(interval):
        time.sleep(interval)

    @staticmethod
    @ExecExceptionHandler(logger)
    def current_time():
        return timezone.now()

    @staticmethod
    @ExecExceptionHandler(logger)
    def future_time(dateconfig, isStrFormat=False, format="%m/%d/%Y, %H:%M:%S %p"):
        dt = Time.current_time()
        return Time.calculate_time(dt, dateconfig, isStrFormat, format)

    @staticmethod
    @ExecExceptionHandler(logger)
    def calculate_time(
        dt, dateconfig, isStrFormat=False, format="%m/%d/%Y, %H:%M:%S %p"
    ):
        td = timedelta(**dateconfig)
        newtime = dt + td
        if not isStrFormat:
            return newtime
        return newtime.strftime(format)

    @staticmethod
    @ExecExceptionHandler(logger)
    def convert_datetime_str(date_str, format="%m/%d/%Y, %H:%M:%S %p"):
        date_obj = datetime.strptime(date_str, format)
        return date_obj
