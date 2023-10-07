from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.handlers.settings.local import LocalHandler
from kfsd.apps.endpoints.handlers.settings.remote import RemoteHandler
from kfsd.apps.endpoints.serializers.settings.config import ConfigModelSerializer
from kfsd.apps.endpoints.serializers.settings.local import LocalModelSerializer
from kfsd.apps.endpoints.serializers.settings.remote import RemoteModelSerializer
from kfsd.apps.models.tables.settings.config import Config
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.utils.system import System


class ConfigHandler(BaseHandler):
    def __init__(self, configIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=ConfigModelSerializer,
            modelClass=Config,
            identifier=configIdentifier,
            isDBFetch=isDBFetch,
        )

    def isLocalConfig(self):
        return DictUtils.get(self.getModelQSData(), "is_local_config")

    def getLookupDimensions(self):
        return DictUtils.get(self.getModelQSData(), "lookup_dimension_keys")

    def getLocalHandler(self):
        localHandler = LocalHandler(self.getModelQS().local.identifier, False)
        localQSData = LocalModelSerializer(instance=self.getModelQS().local)
        localHandler.setModelQSData(localQSData.data)
        localHandler.setModelQS(self.getModelQS().local)
        return localHandler

    def getRemoteHandler(self):
        remoteHandler = RemoteHandler(self.getModelQS().remote.identifier, False)
        remoteQSData = RemoteModelSerializer(instance=self.getModelQS().remote)
        remoteHandler.setModelQSData(remoteQSData.data)
        remoteHandler.setModelQS(self.getModelQS().remote)
        return remoteHandler

    def genConfig(self):
        if self.isLocalConfig():
            return self.getLocalHandler().genConfig(self.constructDimensionsFromEnv())
        else:
            return self.getRemoteHandler().genConfig(self.constructDimensionsFromEnv())

    def constructDimensionsFromEnv(self):
        return {key: System.getEnv(key) for key in self.getLookupDimensions()}
