import json
from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.general.data import DataModelSerializer
from kfsd.apps.models.tables.general.data import Data
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.models.constants import JSON, FILE
from kfsd.apps.core.common.template import Template
from kfsd.apps.endpoints.handlers.general.file import gen_file_handler


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

    def isFileSource(self):
        sourceType = DictUtils.get(self.getModelQSData(), "source_type")
        if sourceType == FILE:
            return True
        return False

    def getDefaultTemplateAttrs(self):
        return DictUtils.get(self.getModelQSData(), "default_template_values")

    def isJson(self):
        contentType = DictUtils.get(self.getModelQSData(), "content_type")
        if contentType == JSON:
            return True
        return False

    def getFileContent(self):
        if not self.getModelQS().file:
            return None

        fileHandler = gen_file_handler(self.getModelQS().file)
        return fileHandler.getFile()

    def getRawBody(self):
        return DictUtils.get(self.getModelQSData(), "raw_body")

    def getRawJsonBody(self):
        return DictUtils.get(self.getModelQSData(), "raw_json_body")

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
        body = None
        if not self.isFileSource():
            body = self.getRawBody()
            if self.isJson():
                body = self.getRawJsonBody()
        else:
            body = self.getFileContent()
            if self.isJson():
                body = json.loads(body)
        if self.isTemplate():
            return self.genTemplate(body, context)
        return body
