from rest_framework.exceptions import APIException
from rest_framework import status
import json
import requests

from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.common.logger import Logger, LogLevel

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class KubefacetsAPIException(APIException):
    default_detail = "Unexpected Error"
    status_code = 500
    default_code = "unexpected_error"
    detailed_msg = ""

    def __init__(self, detail, defaultCode, statusCode, detailedMsg=""):
        self.detail = detail
        self.status_code = statusCode
        self.default_code = defaultCode
        self.detailed_msg = detailedMsg
        logger.error(self.detailed_msg)


def handle_gateway_exception(f):
    def wrapper(*args, **kwargs):
        obj = args[0]
        try:
            resp = f(*args, **kwargs)
            return resp
        except KubefacetsAPIException as e:
            jsonData = {
                "status": False,
                "data": {},
                "error": {
                    "detail": e.detail,
                    "status_code": e.status_code,
                    "default_code": e.default_code,
                    "type": "error",
                    "detailed_msg": e.detailed_msg,
                },
            }
            resp = requests.Response()
            resp.status_code = status.HTTP_504_GATEWAY_TIMEOUT
            resp._content = json.dumps(jsonData).encode("utf-8")
            resp.headers["Content-Type"] = "application/json"
            obj.setResponse(resp)
            obj.getLogger().logWebRequestError(
                obj.getDjangoRequest().getRequest(),
                jsonData,
                DictUtils.get_by_path(jsonData, "error.type"),
            )
            return resp.json()

    return wrapper
