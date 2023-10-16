import urllib.parse
import requests
import urllib3.exceptions
from rest_framework import status

from kfsd.apps.core.exceptions.api import KubefacetsAPIException
from kfsd.apps.core.utils.http.response import Response


class HTTP(Response):
    def formatUrl(self, args):
        if None in args:
            raise KubefacetsAPIException(
                "Invalid url paths passed for forming url",
                "url_error",
                status.HTTP_400_BAD_REQUEST,
                "Probably config error, plz check if services are up?",
            )
        return "/".join(args)

    def genUrlEncode(self, urlstr):
        return urllib.parse.quote(urlstr)

    def request(self, method, url, expStatus, **kwargs):
        try:
            resp = method(url, **kwargs)
            self.setResponse(resp)
            if self.isRespValid(expStatus):
                return resp
        except requests.exceptions.Timeout as e:
            raise KubefacetsAPIException(
                "The server took too long to respond to your request. Please try again later.",
                "server_timed_out",
                status.HTTP_408_REQUEST_TIMEOUT,
                "url: {}, error: {}".format(url, str(e)),
            )
        except requests.exceptions.ConnectionError as e:
            raise KubefacetsAPIException(
                "Service temporarily unavailable. Please try again later.",
                "service_unavailable",
                status.HTTP_503_SERVICE_UNAVAILABLE,
                "url: {}, error: {}".format(url, str(e)),
            )
        except urllib3.exceptions.NewConnectionError as e:
            raise KubefacetsAPIException(
                "Service temporarily unavailable. Please try again later.",
                "service_unavailable",
                status.HTTP_503_SERVICE_UNAVAILABLE,
                "url: {}, error: {}".format(url, str(e)),
            )

    def post(self, url, expStatus, **kwargs):
        return self.request(requests.post, url, expStatus, **kwargs)

    def get(self, url, expStatus, **kwargs):
        return self.request(requests.get, url, expStatus, **kwargs)

    def delete(self, url, expStatus, **kwargs):
        return self.request(requests.delete, url, expStatus, **kwargs)
