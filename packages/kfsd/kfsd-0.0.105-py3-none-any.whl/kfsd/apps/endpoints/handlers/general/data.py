from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.general.data import DataModelSerializer
from kfsd.apps.models.tables.general.data import Data
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.models.constants import JSON
from kfsd.apps.core.common.template import Template


def gen_data_handler(instance):
    handler = DataHandler(instance.identifier, False)
    qsData = DataModelSerializer(instance=instance)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


class DataHandler(BaseHandler):
    def __init__(self, dataIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=DataModelSerializer,
            modelClass=Data,
            identifier=dataIdentifier,
            isDBFetch=isDBFetch,
        )

    def isTemplate(self):
        return DictUtils.get(self.getModelQSData(), "is_template")

    def getDefaultTemplateAttrs(self):
        return DictUtils.get(self.getModelQSData(), "default_template_values")

    def isJson(self):
        contentType = DictUtils.get(self.getModelQSData(), "content_type")
        if contentType == JSON:
            return True
        return False

    def getBody(self):
        return DictUtils.get(self.getModelQSData(), "body")

    def getJsonBody(self):
        return DictUtils.get(self.getModelQSData(), "json_body")

    def genTemplate(self, body, context):
        template = Template(
            body,
            context,
            {},
            False,
            self.getDefaultTemplateAttrs(),
        )
        return template.mergeValues()

    def genBody(self, context):
        body = self.getBody()
        if self.isJson():
            body = self.getJsonBody()
        if self.isTemplate():
            return self.genTemplate(body, context)
        return body
