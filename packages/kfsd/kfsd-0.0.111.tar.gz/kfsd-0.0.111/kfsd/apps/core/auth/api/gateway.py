import requests
import json

from kfsd.apps.core.utils.http.base import HTTP
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.utils.http.django.request import DjangoRequest
from kfsd.apps.core.utils.http.headers.base import Headers
from kfsd.apps.core.utils.http.headers.contenttype import ContentType
from kfsd.apps.core.exceptions.api import KubefacetsAPIException
from kfsd.apps.core.common.logger import Logger, LogLevel

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class APIGateway(Headers, HTTP):
    def __init__(self, request=None):
        self.__request = DjangoRequest(request)
        Headers.__init__(self)
        HTTP.__init__(self)

    def getServicesAPIKey(self):
        return self.getDjangoRequest().findConfigs(["services.api_key"])[0]

    def getDjangoRequest(self):
        return self.__request

    def setErrorResponse(self, e):
        response = requests.models.Response()
        response.status_code = 200
        response.headers = {"Content-Type": "application/json"}
        errorResp = self.constructGatewayResp(False, {}, self.readExceptionError(e))
        response._content = bytes(json.dumps(errorResp), "utf-8")
        self.setResponse(response)
        logger.logWebRequestError(
            self.getDjangoRequest().getRequest(), self.readExceptionError(e), "error"
        )

    def setSuccessResponse(self, resp):
        response = requests.models.Response()
        response.status_code = 200
        response.headers = {"Content-Type": "application/json"}
        successResp = self.constructGatewayResp(True, resp, {})
        response._content = bytes(json.dumps(successResp), "utf-8")
        self.setResponse(response)

    def isHTTPRequestSuccessfull(self):
        return DictUtils.get(self.getJsonResponse(), "status")

    def constructGatewayResp(self, status, data, errors={}):
        return {
            "status": status,
            "data": data,
            "error": errors,
        }

    def readExceptionError(self, e):
        return {
            "detail": e.detail,
            "status_code": e.status_code,
            "default_code": e.default_code,
            "type": "error",
        }

    def setHttpHeaders(self):
        self.setAPIKey(self.getServicesAPIKey())
        self.setContentType(ContentType.APPLICATION_JSON)

    def isGatewayFormatResp(self):
        return DictUtils.key_exists_multi(self.getJsonResponse(), ["status", "data", "error"])

    def httpPost(self, postUrl, payload, expStatus):
        try:
            self.setHttpHeaders()
            self.post(postUrl, expStatus, json=payload, headers=self.getReqHeaders())
            if not self.isGatewayFormatResp():
                self.setSuccessResponse(self.getJsonResponse())
                return self.getJsonResponse()
            return self.getJsonResponse()
        except KubefacetsAPIException as e:
            self.setErrorResponse(e)
            return self.getJsonResponse()

    def httpGet(self, getUrl, expStatus):
        try:
            self.setHttpHeaders()
            self.get(getUrl, expStatus, headers=self.getReqHeaders())
            if not self.isGatewayFormatResp():
                self.setSuccessResponse(self.getJsonResponse())
                return self.getJsonResponse()
            return self.getJsonResponse()
        except KubefacetsAPIException as e:
            self.setErrorResponse(e)
            return self.getJsonResponse()

    def httpDel(self, getUrl, expStatus):
        try:
            self.setHttpHeaders()
            self.delete(getUrl, expStatus, headers=self.getReqHeaders())
            if not self.isGatewayFormatResp():
                self.setSuccessResponse({})
                return self.getJsonResponse()
            return self.getJsonResponse()
        except KubefacetsAPIException as e:
            self.setErrorResponse(e)
            return self.getJsonResponse()

    def constructUrl(self, configPaths):
        uris = self.getDjangoRequest().findConfigs(configPaths)
        return self.formatUrl(uris)
