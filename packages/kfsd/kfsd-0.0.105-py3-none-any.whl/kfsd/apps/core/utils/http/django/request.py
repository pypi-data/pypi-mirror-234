import requests
from django.http import HttpRequest

from kfsd.apps.core.utils.http.django.cookie import Cookie
from kfsd.apps.core.utils.http.django.config import DjangoConfig


class DjangoRequest(DjangoConfig):
    def __init__(self, request=None):
        self.__request = request
        self.__djangoCookies = Cookie(request)
        DjangoConfig.__init__(self, self.getConfigData())

    def getRequest(self):
        return self.__request

    def getDjangoReqCookies(self):
        return self.__djangoCookies

    def parseInputData(self, serializer, raiseExceptions=True):
        inputSerializer = serializer(data=self.__request.data)
        inputSerializer.is_valid(raise_exception=raiseExceptions)
        return inputSerializer.data

    def getConfigData(self):
        return self.__request.config

    @staticmethod
    def genDjangoRequest(url, method):
        request = requests.Request(method, url)
        prepared_request = request.prepare()

        django_request = HttpRequest()
        django_request.method = prepared_request.method
        django_request.path = prepared_request.path_url
        return django_request
