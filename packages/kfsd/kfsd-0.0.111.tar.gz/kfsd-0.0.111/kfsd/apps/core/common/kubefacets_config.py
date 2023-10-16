from kfsd.apps.core.utils.system import System
from kfsd.apps.core.common.cache import cache, DjangoCache
from kfsd.apps.core.common.logger import Logger, LogLevel
from kfsd.apps.core.utils.http.base import HTTP
from kfsd.apps.core.utils.http.headers.base import Headers
from kfsd.apps.endpoints.handlers.settings.setting import SettingHandler
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.models.constants import KEY_CACHE_TIMEOUT
import json

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class KubefacetsConfig(Headers, HTTP):
    DEFAULT_KUBEFACETS_SETTINGS_ID = "SETTING=Kubefacets Settings"

    def __init__(self):
        Headers.__init__(self)
        HTTP.__init__(self)
        self.__config = self.genConfig()
        self.setCacheTimeout()

    def setCacheTimeout(self):
        isCacheEnabled = DictUtils.get_by_path(
            self.__config, "services.features_enabled.cache"
        )
        if isCacheEnabled:
            cacheTimeout = DictUtils.get_by_path(
                self.__config, "services.cache.timeout"
            )
            DjangoCache.set(KEY_CACHE_TIMEOUT, cacheTimeout, cacheTimeout)

    def constructDimensionsFromEnv(self, dimensionKeys):
        return {key: System.getEnv(key) for key in dimensionKeys}

    def getSettingID(self):
        settinsID = System.getEnv("SETTINGS_ID")
        return settinsID if settinsID else self.DEFAULT_KUBEFACETS_SETTINGS_ID

    @cache("kfsd.settings.config")
    def genConfig(self):
        settingIdentifier = self.getSettingID()
        try:
            settingHandler = SettingHandler(settingIdentifier, True)
            configHandler = settingHandler.getConfigHandler()
            config = configHandler.genConfig()
            logger.info("Configuration: {}".format(json.dumps(config, indent=4)))
            return config
        except Exception as e:
            logger.error(
                "Settings for id: {}, resulted in error: {}".format(
                    settingIdentifier, e
                )
            )
            return {}

    def getConfig(self):
        return self.__config
