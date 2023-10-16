from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.requests.template import (
    RequestTemplateModelSerializer,
)
from kfsd.apps.models.tables.requests.template import RequestTemplate


def gen_request_template_handler(instance):
    handler = RequestTemplateHandler(instance.identifier, False)
    qsData = RequestTemplateModelSerializer(instance=instance)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


class RequestTemplateHandler(BaseHandler):
    def __init__(self, templateIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=RequestTemplateModelSerializer,
            modelClass=RequestTemplate,
            identifier=templateIdentifier,
            isDBFetch=isDBFetch,
        )

    def getHeaders(self):
        return self.getModelQS().headers.all()

    def getParams(self):
        return self.getModelQS().params.all()
