from kfsd.apps.core.common.configuration import Configuration
from kfsd.apps.core.common.logger import Logger, LogLevel

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class DjangoConfig:
    def __init__(self, config={}):
        self.__config = config

    def getConfig(self):
        return self.__config

    def findConfigs(self, paths):
        configPaths = Configuration.findConfigValues(self.getConfig(), paths)
        if None in configPaths:
            logger.error(
                "Requested Config Paths: {}, values found: {}".format(
                    paths, configPaths
                )
            )
        return configPaths
