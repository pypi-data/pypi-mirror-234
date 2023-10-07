from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.settings.local import LocalModelSerializer
from kfsd.apps.models.tables.settings.local import Local
from kfsd.apps.core.common.configuration import Configuration
from kfsd.apps.core.utils.dict import DictUtils


class LocalHandler(BaseHandler):
    def __init__(self, localIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=LocalModelSerializer,
            modelClass=Local,
            identifier=localIdentifier,
            isDBFetch=isDBFetch,
        )

    def getData(self):
        return DictUtils.get(self.getModelQSData(), "data")

    def genConfig(self, dimensions):
        config = Configuration(
            settings=self.getData(), dimensions=dimensions
        ).getFinalConfig()
        return config
