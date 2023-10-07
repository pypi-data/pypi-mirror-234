from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.settings.setting import SettingModelSerializer
from kfsd.apps.endpoints.serializers.settings.config import ConfigModelSerializer
from kfsd.apps.endpoints.handlers.settings.config import ConfigHandler
from kfsd.apps.models.tables.settings.setting import Setting
from kfsd.apps.core.utils.dict import DictUtils


class SettingHandler(BaseHandler):
    def __init__(self, settingIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=SettingModelSerializer,
            modelClass=Setting,
            identifier=settingIdentifier,
            isDBFetch=isDBFetch,
        )

    def getConfigId(self):
        return DictUtils.get(self.getModelQSData(), "config")

    def getConfigHandler(self):
        configHandler = ConfigHandler(self.getConfigId(), False)
        configQSData = ConfigModelSerializer(instance=self.getModelQS().config)
        configHandler.setModelQSData(configQSData.data)
        configHandler.setModelQS(self.getModelQS().config)
        return configHandler

    def genConfig(self):
        return self.getConfigHandler().genConfig()
