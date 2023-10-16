import requests
from rest_framework import status

from kfsd.apps.core.exceptions.api import KubefacetsAPIException
from kfsd.apps.core.utils.http.response import Response
from kfsd.apps.core.utils.http.headers.base import Headers


class Request(Headers, Response):
    def __init__(self):
        self.__expStatusCode = None

    def setExpStatusCode(self, code):
        self.__expStatusCode = code

    def request(self, method, url, expStatus, **kwargs):
        try:
            resp = method(url, **kwargs)
            self.setResponse(resp)
            if self.isRespValid(expStatus):
                return resp
        except requests.exceptions.Timeout:
            raise KubefacetsAPIException(
                "The server took too long to respond to your request. Please try again later.",
                "server_timed_out",
                status.HTTP_408_REQUEST_TIMEOUT,
            )
        except requests.exceptions.ConnectionError:
            raise KubefacetsAPIException(
                "Service temporarily unavailable. Please try again later.",
                "service_unavailable",
                status.HTTP_503_SERVICE_UNAVAILABLE,
            )

    def post(self, url, expStatus, **kwargs):
        return self.request(requests.post, url, expStatus, **kwargs)

    def get(self, url, expStatus, **kwargs):
        return self.request(requests.get, url, expStatus, **kwargs)

    def delete(self, url, expStatus, **kwargs):
        return self.request(requests.delete, url, expStatus, **kwargs)
