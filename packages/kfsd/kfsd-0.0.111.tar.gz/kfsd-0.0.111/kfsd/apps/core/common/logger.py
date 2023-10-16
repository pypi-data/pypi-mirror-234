from enum import Enum
from functools import wraps
from kfsd.apps.core.common.singleton import Singleton

import logging
import json


class Logger:
    __defaultFormat = "[%(asctime)s][%(name)s][%(levelname)s] %(message)s"

    def __init__(self, fileName, logLevel, stream=None):
        self.__logger = logging.getLogger(fileName)
        self.__handler = self.setStreamHandler(stream)
        self.__getLoggerLevel(logLevel)
        self.setFormat(self.__defaultFormat)

    @classmethod
    @Singleton
    def getSingleton(cls, fileName, logLevel, stream=None):
        return cls(fileName, logLevel, stream)

    def setStreamHandler(self, stream):
        return logging.StreamHandler(stream)

    def getLogger(self):
        return self.__logger

    def getHandler(self):
        return self.__handler

    def setFormat(self, format):
        formatter = logging.Formatter(format)
        self.__handler.setFormatter(formatter)
        self.__logger.addHandler(self.__handler)

    def __getLogger(self):
        return self.__logger

    def debug(self, msg, *args, **kwargs):
        self.__getLogger().debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.__getLogger().info(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.__getLogger().error(msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        self.__getLogger().warn(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        self.__getLogger().exception(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.__getLogger().critical(msg, *args, **kwargs)

    def __getLoggerLevel(self, logLevel):
        if logLevel is not None:
            loggerLevelDict = {}
            loggerLevelDict[str(LogLevel.CRITICAL)] = logging.CRITICAL
            loggerLevelDict[str(LogLevel.ERROR)] = logging.ERROR
            loggerLevelDict[str(LogLevel.WARNING)] = logging.WARNING
            loggerLevelDict[str(LogLevel.INFO)] = logging.INFO
            loggerLevelDict[str(LogLevel.DEBUG)] = logging.DEBUG
            loggerLevelDict[str(LogLevel.NOTSET)] = logging.NOTSET
            loggingLevel = (
                loggerLevelDict[str(logLevel)]
                if str(logLevel) in loggerLevelDict
                else logging.NOTSET
            )
            return self.__logger.setLevel(loggingLevel)

        return self.__logger.setLevel(logging.NOTSET)

    def getLogMethod(self, errorType):
        logMap = {
            "error": self.error,
            "warn": self.warn,
            "debug": self.debug,
            "info": self.info,
            "critical": self.critical,
        }
        if errorType in logMap:
            return logMap[errorType]
        else:
            return self.error

    def getAttr(self, obj, attr):
        if hasattr(obj, attr):
            return getattr(obj, attr)
        return None

    def logWebRequestError(self, request, error, errorType):
        x_apikey = request.headers["X_Apikey"] if "X_Apikey" in request.headers else ""
        errorData = {
            "request_info": {
                "path": request.build_absolute_uri(),
                "method": self.getAttr(request, "method"),
                "api_key": x_apikey,
                "content_type": self.getAttr(request, "content_type"),
                "query_params": self.getAttr(request, "query_params"),
                "body": self.getAttr(request, "data")
            },
            "error": error,
        }
        errorStr = json.dumps(errorData, indent=4)

        self.getLogMethod(errorType)(errorStr)


class LogLevel(Enum):
    CRITICAL = 0
    ERROR = 1
    WARNING = 2
    INFO = 3
    DEBUG = 4
    NOTSET = 5


def InstanceDebug(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        selfObj = args[0]
        result = func(*args, **kwargs)
        selfObj.getLogObj().debug("Input:{}, Output: {}".format(args, result))
        return result

    return wrapper


def Debug(logger):
    def debugWrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            logger.debug("Input:{}, Output: {}".format(args, result))
            return result

        return wrapper

    return debugWrapper
